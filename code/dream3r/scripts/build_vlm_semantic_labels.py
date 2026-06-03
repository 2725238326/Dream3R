"""Build offline VLM semantic-risk labels for Dream3R controller gates.

This is a controller-signal cache, not a geometry model path. It labels
existing image windows with strict semantic-risk JSON, converts valid records
into Router/Critic-ready numeric features, and emits shuffled/disabled controls
for later causality checks. Invalid VLM output becomes an explicit failure
record; free-form prose is never consumed as training signal.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import random
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Mapping, Optional, Sequence, Tuple


SCHEMA_VERSION = "dream3r_vlm_semantic_v1"
DEFAULT_MODEL_ID = "Qwen/Qwen3-VL-2B-Instruct"

SCENE_TYPES = ("road", "indoor", "forest", "tunnel", "building", "unknown")
RISK_KEYS = (
    "risk_dynamic",
    "risk_low_texture",
    "risk_reflection",
    "risk_occlusion",
    "risk_large_baseline",
    "risk_scale_drift",
    "risk_repeated_structure",
)
SUGGEST_KEYS = ("suggest_verify_geometry", "suggest_expensive_teacher")
VISIBLE_FAILURE_CAUSES = {
    "dynamic",
    "low_texture",
    "reflection",
    "occlusion",
    "large_baseline",
    "scale_drift",
    "repeated_structure",
}
CAUSE_TO_RISK_KEY = {
    "dynamic": "risk_dynamic",
    "low_texture": "risk_low_texture",
    "reflection": "risk_reflection",
    "occlusion": "risk_occlusion",
    "large_baseline": "risk_large_baseline",
    "scale_drift": "risk_scale_drift",
    "repeated_structure": "risk_repeated_structure",
}
CAUSE_RISK_FLOOR = 0.65

BACKEND_OPTIONAL_FIELDS = {"failure_flags"}
BACKEND_REQUIRED_FIELDS = {
    "scene_type",
    *RISK_KEYS,
    "important_objects",
    "visible_failure_causes",
    *SUGGEST_KEYS,
    "confidence",
}
BACKEND_ALLOWED_FIELDS = BACKEND_REQUIRED_FIELDS | BACKEND_OPTIONAL_FIELDS

RECORD_KEYS = (
    "schema_version",
    "model_id",
    "prompt_hash",
    "backend",
    "window_id",
    "dataset",
    "frames",
    "scene_type",
    *RISK_KEYS,
    "important_objects",
    "visible_failure_causes",
    *SUGGEST_KEYS,
    "confidence",
    "failure_flags",
)

SCENE_FEATURE_KEYS = tuple(f"scene_{name}" for name in SCENE_TYPES)
FEATURE_ORDER = (
    *SCENE_FEATURE_KEYS,
    *RISK_KEYS,
    "suggest_verify_geometry",
    "suggest_expensive_teacher",
    "confidence",
    "schema_failure",
)

PROMPT_TEMPLATE = """You are labeling a 4-frame visual-geometry reconstruction window for Dream3R.
Return exactly one raw JSON object matching the requested schema.
Do not wrap it in Markdown or code fences. Do not add explanation text.

Task:
Classify scene type and visual risk factors that may affect 3D reconstruction.
Use the images only. Do not estimate metric depth or camera pose. Do not invent
hidden objects. If uncertain, lower confidence and use "unknown".

Strict field rules:
- Use only JSON booleans true/false for suggest_verify_geometry and
  suggest_expensive_teacher. Do not write explanation strings in these fields.
- visible_failure_causes must contain only these enum tokens:
  dynamic, low_texture, reflection, occlusion, large_baseline, scale_drift,
  repeated_structure. Use [] when no enum fits.
- risk_* and confidence values must be numbers between 0.0 and 1.0.
- If a cause appears in visible_failure_causes, the matching risk_* value must
  be at least 0.5. Do not output all risk_* = 0 when visible objects or texture
  conditions indicate a listed cause.
- suggest_verify_geometry should be true only when at least one risk_* >= 0.5
  or a visible_failure_causes token is present; otherwise false.

Schema:
{
  "scene_type": "road|indoor|forest|tunnel|building|unknown",
  "risk_dynamic": 0.0,
  "risk_low_texture": 0.0,
  "risk_reflection": 0.0,
  "risk_occlusion": 0.0,
  "risk_large_baseline": 0.0,
  "risk_scale_drift": 0.0,
  "risk_repeated_structure": 0.0,
  "important_objects": [],
  "visible_failure_causes": [],
  "suggest_verify_geometry": true,
  "suggest_expensive_teacher": false,
  "confidence": 0.0
}
"""


@dataclass
class BackendResult:
    text: str
    backend: str
    runtime_seconds: float = 0.0
    failure_flags: List[str] = field(default_factory=list)


class MockSemanticBackend:
    """Deterministic local backend for schema and control tests."""

    def __init__(self, mode: str = "valid") -> None:
        if mode not in {"valid", "invalid", "mixed"}:
            raise ValueError(f"unsupported mock mode: {mode}")
        self.mode = mode
        self.name = f"mock_{mode}"

    def label(self, window: Mapping[str, Any], prompt: str) -> BackendResult:
        del prompt
        if self.mode == "invalid" or (
            self.mode == "mixed" and "invalid" in str(window["window_id"]).lower()
        ):
            return BackendResult(
                text="not json; this simulates VLM prose or malformed output",
                backend=self.name,
            )

        window_id = str(window["window_id"]).lower()
        dataset = str(window["dataset"]).lower()
        frames = [str(frame).lower() for frame in window["frames"]]
        joined = " ".join([window_id, dataset, *frames])

        if "tunnel" in joined:
            scene_type = "tunnel"
        elif dataset == "kitti":
            scene_type = "road"
        elif dataset == "eth3d":
            scene_type = "building"
        else:
            scene_type = "unknown"

        risk_dynamic = 0.78 if any(token in joined for token in ("car", "ped", "dynamic")) else 0.32
        risk_low_texture = 0.72 if any(token in joined for token in ("tunnel", "blank", "lowtexture")) else 0.18
        risk_reflection = 0.68 if any(token in joined for token in ("glass", "mirror", "reflect")) else 0.08
        risk_occlusion = 0.58 if any(token in joined for token in ("occlude", "crowd")) else 0.20
        risk_large_baseline = 0.52 if len(window["frames"]) >= 4 else 0.22
        risk_scale_drift = 0.40 if dataset == "eth3d" else 0.24
        risk_repeated_structure = 0.55 if any(token in joined for token in ("building", "corridor")) else 0.16

        causes: List[str] = []
        if risk_dynamic >= 0.5:
            causes.append("dynamic")
        if risk_low_texture >= 0.5:
            causes.append("low_texture")
        if risk_reflection >= 0.5:
            causes.append("reflection")
        if risk_occlusion >= 0.5:
            causes.append("occlusion")
        if risk_large_baseline >= 0.5:
            causes.append("large_baseline")
        if risk_scale_drift >= 0.5:
            causes.append("scale_drift")
        if risk_repeated_structure >= 0.5:
            causes.append("repeated_structure")

        payload = {
            "scene_type": scene_type,
            "risk_dynamic": risk_dynamic,
            "risk_low_texture": risk_low_texture,
            "risk_reflection": risk_reflection,
            "risk_occlusion": risk_occlusion,
            "risk_large_baseline": risk_large_baseline,
            "risk_scale_drift": risk_scale_drift,
            "risk_repeated_structure": risk_repeated_structure,
            "important_objects": ["car"] if risk_dynamic >= 0.5 else [],
            "visible_failure_causes": causes,
            "suggest_verify_geometry": bool(causes),
            "suggest_expensive_teacher": risk_large_baseline >= 0.5 or risk_reflection >= 0.5,
            "confidence": 0.86 if causes else 0.74,
        }
        return BackendResult(text=json.dumps(payload), backend=self.name)


class QwenSemanticBackend:
    """Optional Qwen3-VL backend with local-files-only default.

    The model is loaded lazily. Unless ``allow_remote_model_load`` is true,
    Hugging Face loading is forced to local files only, which prevents this
    script from downloading checkpoints as a side effect.
    """

    def __init__(
        self,
        model_id: str = DEFAULT_MODEL_ID,
        model_path: Optional[str] = None,
        max_new_tokens: int = 256,
        allow_remote_model_load: bool = False,
    ) -> None:
        self.model_id = model_id
        self.model_source = model_path or model_id
        self.max_new_tokens = int(max_new_tokens)
        self.local_files_only = not bool(allow_remote_model_load)
        self.name = "qwen3vl2b"
        self._processor = None
        self._model = None

    def _load(self) -> None:
        if self._model is not None and self._processor is not None:
            return
        try:
            from transformers import AutoModelForImageTextToText, AutoProcessor
        except Exception as exc:  # pragma: no cover - depends on optional install
            raise RuntimeError(
                "Qwen backend requires transformers with Qwen3-VL support"
            ) from exc

        load_kwargs = {
            "dtype": "auto",
            "device_map": "auto",
            "local_files_only": self.local_files_only,
        }
        try:
            self._model = AutoModelForImageTextToText.from_pretrained(
                self.model_source,
                **load_kwargs,
            )
        except TypeError:  # pragma: no cover - older transformers compatibility
            load_kwargs.pop("dtype", None)
            self._model = AutoModelForImageTextToText.from_pretrained(
                self.model_source,
                **load_kwargs,
            )
        self._processor = AutoProcessor.from_pretrained(
            self.model_source,
            local_files_only=self.local_files_only,
        )

    def label(self, window: Mapping[str, Any], prompt: str) -> BackendResult:
        self._load()
        assert self._model is not None
        assert self._processor is not None

        content = [
            {"type": "image", "image": str(frame)}
            for frame in window["frames"]
        ]
        content.append({"type": "text", "text": prompt})
        messages = [{"role": "user", "content": content}]

        started = time.time()
        inputs = self._processor.apply_chat_template(
            messages,
            tokenize=True,
            add_generation_prompt=True,
            return_dict=True,
            return_tensors="pt",
        )
        device = getattr(self._model, "device", None)
        if device is not None:
            inputs = inputs.to(device)
        generated_ids = self._model.generate(
            **inputs,
            max_new_tokens=self.max_new_tokens,
            do_sample=False,
        )
        input_ids = inputs["input_ids"]
        trimmed = [
            out_ids[len(in_ids):]
            for in_ids, out_ids in zip(input_ids, generated_ids)
        ]
        output_text = self._processor.batch_decode(
            trimmed,
            skip_special_tokens=True,
            clean_up_tokenization_spaces=False,
        )[0]
        return BackendResult(
            text=output_text,
            backend=self.name,
            runtime_seconds=time.time() - started,
        )


def prompt_hash(prompt: str = PROMPT_TEMPLATE) -> str:
    return hashlib.sha256(prompt.encode("utf-8")).hexdigest()[:16]


def _normalize_dataset(value: Any) -> str:
    dataset = str(value).lower()
    if dataset.startswith("kitti"):
        return "kitti"
    if dataset.startswith("eth3d"):
        return "eth3d"
    raise ValueError(f"unsupported dataset: {value}")


def load_window_manifest(path: str, max_windows: int = 0) -> List[Dict[str, Any]]:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    if isinstance(data, list):
        rows = data
    elif isinstance(data, dict):
        if isinstance(data.get("windows"), list):
            rows = data["windows"]
        elif isinstance(data.get("records"), list):
            rows = data["records"]
        else:
            raise ValueError("manifest must contain a windows or records list")
    else:
        raise ValueError("manifest must be a JSON list or object")

    windows: List[Dict[str, Any]] = []
    for idx, row in enumerate(rows):
        if not isinstance(row, dict):
            raise ValueError(f"manifest row {idx} is not an object")
        window_id = row.get("window_id") or row.get("id") or row.get("seq")
        dataset = row.get("dataset") or row.get("domain")
        frames = row.get("frames") or row.get("image_paths") or row.get("images")
        if not window_id:
            raise ValueError(f"manifest row {idx} missing window_id")
        if not dataset:
            raise ValueError(f"manifest row {idx} missing dataset/domain")
        if not isinstance(frames, list) or not frames:
            raise ValueError(f"manifest row {idx} missing non-empty frames list")
        if any(not isinstance(frame, str) or not frame for frame in frames):
            raise ValueError(f"manifest row {idx} has invalid frame path")
        windows.append({
            "window_id": str(window_id),
            "dataset": _normalize_dataset(dataset),
            "frames": [str(frame) for frame in frames],
        })
    if max_windows > 0:
        windows = windows[:max_windows]
    return windows


def _base_record(
    window: Mapping[str, Any],
    model_id: str,
    prompt_hash_value: str,
    backend: str,
) -> Dict[str, Any]:
    return {
        "schema_version": SCHEMA_VERSION,
        "model_id": model_id,
        "prompt_hash": prompt_hash_value,
        "backend": backend,
        "window_id": str(window["window_id"]),
        "dataset": _normalize_dataset(window["dataset"]),
        "frames": [str(frame) for frame in window["frames"]],
        "scene_type": "unknown",
        "risk_dynamic": 0.0,
        "risk_low_texture": 0.0,
        "risk_reflection": 0.0,
        "risk_occlusion": 0.0,
        "risk_large_baseline": 0.0,
        "risk_scale_drift": 0.0,
        "risk_repeated_structure": 0.0,
        "important_objects": [],
        "visible_failure_causes": [],
        "suggest_verify_geometry": False,
        "suggest_expensive_teacher": False,
        "confidence": 0.0,
        "failure_flags": [],
    }


def failure_record(
    window: Mapping[str, Any],
    model_id: str,
    prompt_hash_value: str,
    backend: str,
    failure_flags: Sequence[str],
) -> Dict[str, Any]:
    record = _base_record(window, model_id, prompt_hash_value, backend)
    record["failure_flags"] = sorted(set(str(flag) for flag in failure_flags if flag))
    if not record["failure_flags"]:
        record["failure_flags"] = ["unknown_failure"]
    return record


def _json_payload(text: str) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
    text = text.strip()
    if text.startswith("```") and text.endswith("```"):
        lines = text.splitlines()
        if lines and lines[0].strip().startswith("```") and lines[-1].strip() == "```":
            text = "\n".join(lines[1:-1]).strip()
    try:
        payload = json.loads(text)
    except json.JSONDecodeError as exc:
        return None, f"invalid_json:{exc.msg}"
    if not isinstance(payload, dict):
        return None, "invalid_json:not_object"
    return payload, None


def _unit_float(payload: Mapping[str, Any], key: str, errors: List[str]) -> float:
    value = payload.get(key)
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        errors.append(f"{key}:not_number")
        return 0.0
    value = float(value)
    if not math.isfinite(value) or value < 0.0 or value > 1.0:
        errors.append(f"{key}:not_unit_interval")
        return 0.0
    return value


def _bool_value(payload: Mapping[str, Any], key: str, errors: List[str]) -> bool:
    value = payload.get(key)
    if not isinstance(value, bool):
        errors.append(f"{key}:not_bool")
        return False
    return bool(value)


def _string_list(payload: Mapping[str, Any], key: str, errors: List[str]) -> List[str]:
    value = payload.get(key)
    if not isinstance(value, list):
        errors.append(f"{key}:not_list")
        return []
    result: List[str] = []
    for idx, item in enumerate(value):
        if not isinstance(item, str) or not item.strip():
            errors.append(f"{key}[{idx}]:not_nonempty_string")
            continue
        result.append(item.strip())
    return result


def validate_semantic_payload(
    payload: Mapping[str, Any],
    window: Mapping[str, Any],
    model_id: str = DEFAULT_MODEL_ID,
    prompt_hash_value: Optional[str] = None,
    backend: str = "unknown",
) -> Dict[str, Any]:
    prompt_hash_value = prompt_hash_value or prompt_hash()
    errors: List[str] = []
    keys = set(payload)
    missing = sorted(BACKEND_REQUIRED_FIELDS - keys)
    extra = sorted(keys - BACKEND_ALLOWED_FIELDS)
    if missing:
        errors.append("missing_fields:" + ",".join(missing))
    if extra:
        errors.append("unexpected_fields:" + ",".join(extra))

    scene_type = payload.get("scene_type")
    if scene_type not in SCENE_TYPES:
        errors.append("scene_type:not_allowlisted")

    risk_values = {key: _unit_float(payload, key, errors) for key in RISK_KEYS}
    important_objects = _string_list(payload, "important_objects", errors)
    visible_failure_causes = _string_list(payload, "visible_failure_causes", errors)
    unknown_causes = sorted(set(visible_failure_causes) - VISIBLE_FAILURE_CAUSES)
    if unknown_causes:
        errors.append("visible_failure_causes:not_allowlisted:" + ",".join(unknown_causes))
    suggest_values = {key: _bool_value(payload, key, errors) for key in SUGGEST_KEYS}
    confidence = _unit_float(payload, "confidence", errors)

    backend_failure_flags = payload.get("failure_flags", [])
    if backend_failure_flags:
        if not isinstance(backend_failure_flags, list) or any(
            not isinstance(flag, str) or not flag for flag in backend_failure_flags
        ):
            errors.append("failure_flags:not_string_list")
        else:
            errors.extend(f"backend:{flag}" for flag in backend_failure_flags)

    if errors:
        return failure_record(window, model_id, prompt_hash_value, backend, errors)

    record = _base_record(window, model_id, prompt_hash_value, backend)
    record.update(risk_values)
    record.update(suggest_values)
    record["scene_type"] = str(scene_type)
    record["important_objects"] = important_objects
    record["visible_failure_causes"] = visible_failure_causes
    record["confidence"] = confidence
    return record


def validate_record_schema(record: Mapping[str, Any]) -> List[str]:
    errors: List[str] = []
    keys = set(record)
    if keys != set(RECORD_KEYS):
        missing = sorted(set(RECORD_KEYS) - keys)
        extra = sorted(keys - set(RECORD_KEYS))
        if missing:
            errors.append("record_missing_fields:" + ",".join(missing))
        if extra:
            errors.append("record_unexpected_fields:" + ",".join(extra))
    if record.get("schema_version") != SCHEMA_VERSION:
        errors.append("schema_version:mismatch")
    if record.get("scene_type") not in SCENE_TYPES:
        errors.append("scene_type:not_allowlisted")
    for key in RISK_KEYS:
        _unit_float(record, key, errors)
    _unit_float(record, "confidence", errors)
    for key in SUGGEST_KEYS:
        _bool_value(record, key, errors)
    _string_list(record, "important_objects", errors)
    causes = _string_list(record, "visible_failure_causes", errors)
    unknown_causes = sorted(set(causes) - VISIBLE_FAILURE_CAUSES)
    if unknown_causes:
        errors.append("visible_failure_causes:not_allowlisted:" + ",".join(unknown_causes))
    flags = record.get("failure_flags")
    if not isinstance(flags, list) or any(not isinstance(flag, str) for flag in flags):
        errors.append("failure_flags:not_string_list")
    frames = record.get("frames")
    if not isinstance(frames, list) or any(not isinstance(frame, str) for frame in frames):
        errors.append("frames:not_string_list")
    try:
        _normalize_dataset(record.get("dataset"))
    except ValueError as exc:
        errors.append(str(exc))
    return errors


def record_to_feature_vector(record: Mapping[str, Any]) -> List[float]:
    scene_type = str(record.get("scene_type", "unknown"))
    scene_values = [1.0 if scene_type == name else 0.0 for name in SCENE_TYPES]
    risk_by_key = {key: float(record[key]) for key in RISK_KEYS}
    for cause in record.get("visible_failure_causes") or []:
        risk_key = CAUSE_TO_RISK_KEY.get(str(cause))
        if risk_key is not None:
            risk_by_key[risk_key] = max(risk_by_key[risk_key], CAUSE_RISK_FLOOR)
    risk_values = [risk_by_key[key] for key in RISK_KEYS]
    suggest_values = [1.0 if bool(record[key]) else 0.0 for key in SUGGEST_KEYS]
    schema_failure = 1.0 if record.get("failure_flags") else 0.0
    return [
        *scene_values,
        *risk_values,
        *suggest_values,
        float(record["confidence"]),
        schema_failure,
    ]


def build_feature_controls(
    records: Sequence[Mapping[str, Any]],
    shuffle_seed: int = 7,
) -> Dict[str, Any]:
    feature_by_window = {
        str(record["window_id"]): record_to_feature_vector(record)
        for record in records
    }
    window_ids = [str(record["window_id"]) for record in records]
    vectors = [feature_by_window[window_id] for window_id in window_ids]
    shuffled_vectors = list(vectors)
    rng = random.Random(shuffle_seed)
    rng.shuffle(shuffled_vectors)
    if len(shuffled_vectors) > 1 and shuffled_vectors == vectors:
        shuffled_vectors = shuffled_vectors[1:] + shuffled_vectors[:1]
    shuffled = {
        window_id: list(shuffled_vectors[idx])
        for idx, window_id in enumerate(window_ids)
    }
    disabled = {
        window_id: [0.0] * len(FEATURE_ORDER)
        for window_id in window_ids
    }
    return {
        "feature_order": list(FEATURE_ORDER),
        "features": feature_by_window,
        "shuffled_features": shuffled,
        "disabled_features": disabled,
        "shuffle_seed": int(shuffle_seed),
        "feature_groups": {
            "scene_one_hot": list(SCENE_FEATURE_KEYS),
            "risk_vector": list(RISK_KEYS),
            "risk_derivation": ["visible_failure_causes_floor"],
            "suggestions": list(SUGGEST_KEYS),
            "validity": ["schema_failure"],
        },
    }


def _schema_report(
    records: Sequence[Mapping[str, Any]],
    model_id: str,
    prompt_hash_value: str,
    backend: str,
    output: str,
    qwen_attempted: bool,
) -> Dict[str, Any]:
    record_errors = {
        str(record["window_id"]): validate_record_schema(record)
        for record in records
    }
    invalid_record_schema = {
        window_id: errors
        for window_id, errors in record_errors.items()
        if errors
    }
    failure_records = [
        record for record in records
        if record.get("failure_flags")
    ]
    valid_records = len(records) - len(failure_records)
    flag_counts: Dict[str, int] = {}
    for record in failure_records:
        for flag in record.get("failure_flags", []):
            flag_counts[str(flag)] = flag_counts.get(str(flag), 0) + 1
    return {
        "schema_version": SCHEMA_VERSION,
        "model_id": model_id,
        "prompt_hash": prompt_hash_value,
        "backend": backend,
        "output": output,
        "qwen_attempted": bool(qwen_attempted),
        "n_windows": len(records),
        "valid_records": valid_records,
        "failure_records": len(failure_records),
        "schema_pass_rate": (valid_records / len(records)) if records else 0.0,
        "invalid_record_schema": invalid_record_schema,
        "failure_flag_counts": flag_counts,
        "feature_order": list(FEATURE_ORDER),
        "control_keys": ["features", "shuffled_features", "disabled_features"],
    }


def _backend_from_args(
    backend: str,
    mock_mode: str,
    model_id: str,
    model_path: Optional[str],
    max_new_tokens: int,
    allow_remote_model_load: bool,
):
    if backend == "mock":
        return MockSemanticBackend(mode=mock_mode)
    if backend == "qwen":
        return QwenSemanticBackend(
            model_id=model_id,
            model_path=model_path,
            max_new_tokens=max_new_tokens,
            allow_remote_model_load=allow_remote_model_load,
        )
    raise ValueError(f"unsupported backend: {backend}")


def build_vlm_semantic_labels(
    window_manifest: str,
    output: str,
    schema_report: Optional[str] = None,
    backend: str = "mock",
    mock_mode: str = "valid",
    model_id: str = DEFAULT_MODEL_ID,
    model_path: Optional[str] = None,
    max_windows: int = 0,
    shuffle_seed: int = 7,
    max_new_tokens: int = 256,
    allow_remote_model_load: bool = False,
) -> Dict[str, Any]:
    windows = load_window_manifest(window_manifest, max_windows=max_windows)
    prompt_hash_value = prompt_hash()
    label_backend = _backend_from_args(
        backend,
        mock_mode,
        model_id,
        model_path,
        max_new_tokens,
        allow_remote_model_load,
    )

    records: List[Dict[str, Any]] = []
    runtime_by_window: Dict[str, float] = {}
    for window in windows:
        try:
            result = label_backend.label(window, PROMPT_TEMPLATE)
            runtime_by_window[str(window["window_id"])] = float(result.runtime_seconds)
            payload, parse_error = _json_payload(result.text)
            if parse_error is not None or payload is None:
                records.append(
                    failure_record(
                        window,
                        model_id,
                        prompt_hash_value,
                        result.backend,
                        [parse_error or "invalid_json"],
                    )
                )
                continue
            record = validate_semantic_payload(
                payload,
                window,
                model_id=model_id,
                prompt_hash_value=prompt_hash_value,
                backend=result.backend,
            )
            if result.failure_flags:
                record["failure_flags"] = sorted(
                    set(record.get("failure_flags", [])) | set(result.failure_flags)
                )
            records.append(record)
        except Exception as exc:
            records.append(
                failure_record(
                    window,
                    model_id,
                    prompt_hash_value,
                    getattr(label_backend, "name", backend),
                    [f"backend_error:{type(exc).__name__}:{exc}"],
                )
            )

    controls = build_feature_controls(records, shuffle_seed=shuffle_seed)
    report = _schema_report(
        records,
        model_id=model_id,
        prompt_hash_value=prompt_hash_value,
        backend=getattr(label_backend, "name", backend),
        output=output,
        qwen_attempted=(backend == "qwen"),
    )
    cache = {
        "schema_version": SCHEMA_VERSION,
        "model_id": model_id,
        "prompt_hash": prompt_hash_value,
        "prompt_template": PROMPT_TEMPLATE,
        "backend": getattr(label_backend, "name", backend),
        "window_manifest": window_manifest,
        "records": records,
        "features": controls["features"],
        "controls": {
            "feature_order": controls["feature_order"],
            "feature_groups": controls["feature_groups"],
            "shuffled_features": controls["shuffled_features"],
            "disabled_features": controls["disabled_features"],
            "shuffle_seed": controls["shuffle_seed"],
            "causality_note": (
                "Use features vs shuffled_features vs disabled_features for "
                "Router/Critic VLM-label causality controls; no geometry is stored here."
            ),
        },
        "runtime_seconds_by_window": runtime_by_window,
        "schema_report": report,
    }

    output_path = Path(output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(cache, indent=2), encoding="utf-8")
    if schema_report:
        report_path = Path(schema_report)
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    return cache


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--window-manifest", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--schema-report", default=None)
    parser.add_argument("--backend", choices=["mock", "qwen"], default="mock")
    parser.add_argument("--mock-mode", choices=["valid", "invalid", "mixed"], default="valid")
    parser.add_argument("--model-id", default=DEFAULT_MODEL_ID)
    parser.add_argument("--model-path", default=None)
    parser.add_argument("--max-windows", type=int, default=0)
    parser.add_argument("--shuffle-seed", type=int, default=7)
    parser.add_argument("--max-new-tokens", type=int, default=256)
    parser.add_argument(
        "--allow-remote-model-load",
        action="store_true",
        help="Allow transformers to resolve remote weights. Requires active approval.",
    )
    args = parser.parse_args()

    cache = build_vlm_semantic_labels(
        window_manifest=args.window_manifest,
        output=args.output,
        schema_report=args.schema_report,
        backend=args.backend,
        mock_mode=args.mock_mode,
        model_id=args.model_id,
        model_path=args.model_path,
        max_windows=args.max_windows,
        shuffle_seed=args.shuffle_seed,
        max_new_tokens=args.max_new_tokens,
        allow_remote_model_load=args.allow_remote_model_load,
    )
    print(json.dumps(cache["schema_report"], indent=2))


if __name__ == "__main__":
    main()

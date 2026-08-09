# core/scanner.py
from __future__ import annotations

import hashlib
import os
from pathlib import Path

from core.entities.ai_model import AIModel, ModelFormat, ModelStatus
from core.exceptions import WorkspaceNotFoundError, ScanFailedError
from core.interfaces.model_repository import ModelRepository


class ModelScanner:
    """
    Escaneia o workspace em busca de arquivos de modelo.
    Registra novos modelos encontrados e remove registros órfãos.
    Não conhece SQLite — depende apenas de ModelRepository.
    """

    SUPPORTED_EXTENSIONS: frozenset[str] = frozenset({
        ".gguf", ".onnx", ".safetensors", ".pt", ".pth", ".bin",
    })

    def __init__(self, repository: ModelRepository) -> None:
        self._repository = repository

    # ── API pública ────────────────────────────────────────────────────────

    def scan(self, workspace_path: str | Path) -> ScanResult:
        """
        Escaneia o workspace e sincroniza com o repositório.
        Retorna um resumo do que foi encontrado, adicionado e removido.
        """
        path = Path(workspace_path)

        if not path.exists():
            raise WorkspaceNotFoundError(str(path))

        try:
            found_files = self._discover_files(path)
            registered  = {m.id: m for m in self._repository.find_all()}

            added   = self._register_new(found_files, registered)
            removed = self._remove_orphans(found_files, registered)

        except WorkspaceNotFoundError:
            raise
        except Exception as exc:
            raise ScanFailedError(str(path), str(exc)) from exc

        return ScanResult(added=added, removed=removed, total=len(found_files))

    def is_supported(self, path: str | Path) -> bool:
        return Path(path).suffix.lower() in self.SUPPORTED_EXTENSIONS

    # ── internos ───────────────────────────────────────────────────────────

    def _discover_files(self, root: Path) -> dict[str, Path]:
        """Retorna {model_id: path} para cada arquivo suportado."""
        files: dict[str, Path] = {}
        for filepath in root.rglob("*"):
            if filepath.is_file() and self.is_supported(filepath):
                model_id = self._make_id(filepath)
                files[model_id] = filepath
        return files

    def _register_new(
        self,
        found: dict[str, Path],
        registered: dict[str, AIModel],
    ) -> list[AIModel]:
        added: list[AIModel] = []
        for model_id, filepath in found.items():
            if model_id not in registered:
                model = self._build_model(model_id, filepath)
                self._repository.save(model)
                added.append(model)
        return added

    def _remove_orphans(
        self,
        found: dict[str, Path],
        registered: dict[str, AIModel],
    ) -> list[AIModel]:
        removed: list[AIModel] = []
        for model_id, model in registered.items():
            if model_id not in found:
                self._repository.delete(model_id)
                removed.append(model)
        return removed

    @staticmethod
    def _build_model(model_id: str, filepath: Path) -> AIModel:
        return AIModel(
            id=model_id,
            name=filepath.stem,
            path=str(filepath),
            format=ModelFormat.from_extension(filepath),
            size_bytes=filepath.stat().st_size,
            status=ModelStatus.READY,
        )

    @staticmethod
    def _make_id(filepath: Path) -> str:
        """ID determinístico baseado no caminho absoluto."""
        return hashlib.sha1(str(filepath.resolve()).encode()).hexdigest()[:16]


class ScanResult:
    __slots__ = ("added", "removed", "total")

    def __init__(
        self,
        added: list[AIModel],
        removed: list[AIModel],
        total: int,
    ) -> None:
        self.added   = added
        self.removed = removed
        self.total   = total

    def __repr__(self) -> str:  # pragma: no cover
        return (
            f"ScanResult(total={self.total}, "
            f"added={len(self.added)}, removed={len(self.removed)})"
        )
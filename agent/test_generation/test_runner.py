import shutil
import subprocess
from pathlib import Path
from typing import List, Optional


def sync_generated_features_to_test_engine(
    *,
    run_dir: Path,
    test_engine_dir: Path,
    engine_features_subdir: str = "Features",
) -> List[Path]:
    """
    Copia/sincroniza `.feature` gerados (em outputs/<run>/tests/generated_features)
    para o `test_engine`, para que o Reqnroll os descubra.
    """
    source_dir = run_dir / "tests" / "generated_features"
    if not source_dir.exists():
        return []

    target_dir = test_engine_dir / engine_features_subdir / "generated"
    target_dir.mkdir(parents=True, exist_ok=True)

    copied: List[Path] = []
    for feature_file in source_dir.glob("*.feature"):
        dest = target_dir / feature_file.name
        shutil.copy2(feature_file, dest)
        copied.append(dest)

    return copied


def run_test_engine(
    *,
    test_engine_dir: Path,
    extra_env: Optional[dict] = None,
) -> int:
    """
    Executa `dotnet test` no `test_engine`.

    Nota: este runner existe para futura integração no pipeline; não tenta gerir
    dependências externas (URL/app) — isso deve ser configurado por env/config.
    """
    env = None
    if extra_env:
        env = {**dict(**subprocess.os.environ), **extra_env}  # type: ignore[attr-defined]

    result = subprocess.run(
        ["dotnet", "test"],
        cwd=str(test_engine_dir),
        env=env,
        check=False,
    )
    return result.returncode


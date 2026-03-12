from typing import Dict, Any, List

from agent.utils import normalize_text, ALLOWED_LABELS


def validate_plan(plan: Dict[str, Any], user_prompt: str) -> List[str]:
    errors: List[str] = []

    issues = plan.get("issues", [])
    requirements = plan.get("requirements", [])

    if not (3 <= len(issues) <= 6):
        errors.append(f"O plano deve ter entre 3 e 6 issues e devolveu {len(issues)}.")

    seen_titles = set()
    normalized_titles = []

    for issue in issues:
        title = issue.get("title", "").strip()
        labels = issue.get("labels", [])

        if not title:
            errors.append("Existe uma issue sem título.")
            continue

        normalized_title = normalize_text(title)

        if normalized_title in seen_titles:
            errors.append(f"Título repetido ou duplicado: '{title}'.")
        else:
            seen_titles.add(normalized_title)

        normalized_titles.append((title, normalized_title))

        invalid_labels = [label for label in labels if label not in ALLOWED_LABELS]
        if invalid_labels:
            errors.append(
                f"A issue '{title}' contém labels inválidas: {', '.join(invalid_labels)}."
            )

    for i in range(len(normalized_titles)):
        for j in range(i + 1, len(normalized_titles)):
            title_a, norm_a = normalized_titles[i]
            title_b, norm_b = normalized_titles[j]

            words_a = set(norm_a.split())
            words_b = set(norm_b.split())

            if words_a and words_b:
                overlap = len(words_a & words_b) / max(len(words_a), len(words_b))
                if overlap >= 0.8:
                    errors.append(
                        f"As issues '{title_a}' e '{title_b}' parecem demasiado semelhantes."
                    )

    issue_text = " ".join(
        normalize_text(
            f"{issue.get('title', '')} {issue.get('body', '')} {' '.join(issue.get('acceptance_criteria', []))}"
        )
        for issue in issues
    )

    for req in requirements:
        req_norm = normalize_text(req)
        req_words = [word for word in req_norm.split() if len(word) > 3]

        if req_words and not any(word in issue_text for word in req_words):
            errors.append(f"O requisito '{req}' pode não estar coberto pelas issues.")

    prompt_norm = normalize_text(user_prompt)
    if "apenas frontend" in prompt_norm or "so frontend" in prompt_norm:
        for issue in issues:
            labels = issue.get("labels", [])
            if "backend" in labels:
                errors.append(
                    f"A issue '{issue.get('title', '')}' inclui backend num pedido apenas frontend."
                )

    return errors
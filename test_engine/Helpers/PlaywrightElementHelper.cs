using Microsoft.Playwright;

namespace FunctionalTests.Helpers;

/// <summary>
/// Helper de localização de elementos Playwright por múltiplas estratégias.
///
/// Estratégia de localização (ordem obrigatória):
///   1. placeholder  — GetByPlaceholder(hint)
///   2. label        — GetByLabel(hint)
///   3. texto visível— GetByText(hint, exact) depois GetByText(hint, partial)
///   4. data-testid  — [data-testid="hint"]
///   5. data-cy      — [data-cy="hint"]
///   6. CSS selector — page.Locator(hint)  (fallback genérico)
///
/// O método principal é FindElementAsync(IPage, string).
/// Use-o em todos os steps que interagem com o DOM.
/// </summary>
public static class PlaywrightElementHelper
{
    /// <summary>
    /// Tempo máximo (ms) para cada tentativa individual de localização.
    /// Valor baixo para que estratégias que falham não bloqueiem demasiado tempo.
    /// </summary>
    private const int QuickTimeout = 1500;

    // ─── API pública ────────────────────────────────────────────────────────

    /// <summary>
    /// Localiza um elemento na página usando a cadeia de estratégias definida.
    /// Ordem: placeholder → label → texto visível → data-testid → data-cy → CSS selector.
    /// </summary>
    /// <param name="page">A página Playwright activa.</param>
    /// <param name="hint">Placeholder, label, texto visível, data-testid, data-cy, ou CSS selector.</param>
    /// <returns>O primeiro locator encontrado e visível.</returns>
    /// <exception cref="InvalidOperationException">
    /// Se nenhuma estratégia encontrar um elemento visível.
    /// </exception>
    public static async Task<ILocator> FindElementAsync(IPage page, string hint)
    {
        var strategies = new (string Name, Func<ILocator> Fn)[]
        {
            // 1. Placeholder
            ("placeholder",      () => page.GetByPlaceholder(hint)),
            // 2. Label associada ao campo
            ("label",            () => page.GetByLabel(hint)),
            // 3. Texto visível — exacto primeiro, parcial depois
            ("text[exact]",      () => page.GetByText(hint, new() { Exact = true })),
            ("text[partial]",    () => page.GetByText(hint, new() { Exact = false })),
            // 4. data-testid
            ("data-testid",      () => page.GetByTestId(hint)),
            // 5. data-cy
            ("data-cy",          () => page.Locator($"[data-cy='{hint}']")),
            // 6. CSS / ARIA / qualquer selector Playwright
            ("css",              () => page.Locator(hint)),
        };

        var locator = await TryStrategiesAsync(hint, strategies);

        if (locator is null)
        {
            throw new InvalidOperationException(
                $"[PlaywrightElementHelper] Não foi possível encontrar o elemento '{hint}'. " +
                "Estratégias tentadas: placeholder, label, texto visível (exacto/parcial), " +
                "data-testid, data-cy, CSS selector.");
        }

        return locator;
    }

    /// <summary>
    /// Verifica se existe pelo menos um elemento visível que corresponda ao hint.
    /// Usa a mesma cadeia de estratégias de FindElementAsync mas não lança excepção — devolve bool.
    /// </summary>
    public static async Task<bool> IsElementVisibleAsync(IPage page, string hint)
    {
        var strategies = new (string Name, Func<ILocator> Fn)[]
        {
            ("placeholder",   () => page.GetByPlaceholder(hint)),
            ("label",         () => page.GetByLabel(hint)),
            ("text[exact]",   () => page.GetByText(hint, new() { Exact = true })),
            ("text[partial]", () => page.GetByText(hint, new() { Exact = false })),
            ("data-testid",   () => page.GetByTestId(hint)),
            ("data-cy",       () => page.Locator($"[data-cy='{hint}']")),
            ("css",           () => page.Locator(hint)),
        };

        var locator = await TryStrategiesAsync(hint, strategies);
        return locator is not null;
    }

    // ─── Implementação interna ────────────────────────────────────────────────

    private static async Task<ILocator?> TryStrategiesAsync(
        string hint,
        (string Name, Func<ILocator> Fn)[] strategies)
    {
        foreach (var (name, fn) in strategies)
        {
            try
            {
                var locator = fn();

                await locator.First.WaitForAsync(new LocatorWaitForOptions
                {
                    State = WaitForSelectorState.Visible,
                    Timeout = QuickTimeout,
                });

                Console.WriteLine($"[PlaywrightElementHelper] '{hint}' encontrado via {name}");
                return locator.First;
            }
            catch
            {
                // Esta estratégia não encontrou o elemento — tenta a próxima.
            }
        }

        return null;
    }
}

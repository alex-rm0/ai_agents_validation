using Microsoft.Playwright;

namespace FunctionalTests.Helpers;

/// <summary>
/// Helper de localização de elementos Playwright por múltiplas estratégias.
/// Ordem de tentativa para campos de input:
///   1. GetByLabel (label associada ao campo)
///   2. GetByPlaceholder (atributo placeholder)
///   3. [data-testid="hint"]
///   4. [data-cy="hint"]
///   5. hint como CSS selector
///
/// Ordem de tentativa para elementos clicáveis:
///   1. GetByRole(Button, Name)
///   2. GetByRole(Link, Name)
///   3. GetByText (texto exacto)
///   4. GetByText (texto parcial)
///   5. [data-testid="hint"]
///   6. [data-cy="hint"]
///   7. hint como CSS selector
/// </summary>
public static class PlaywrightElementHelper
{
    /// <summary>
    /// Tempo máximo (ms) para cada tentativa individual de localização.
    /// Valor baixo para não bloquear muito tempo em estratégias que não funcionam.
    /// </summary>
    private const int QuickTimeout = 1500;

    /// <summary>
    /// Localiza um campo de input para preenchimento (Fill).
    /// Tenta por: label, placeholder, data-testid, data-cy, CSS selector.
    /// </summary>
    /// <param name="page">A página Playwright activa.</param>
    /// <param name="hint">Label, placeholder, data-testid, data-cy, ou CSS selector do campo.</param>
    /// <returns>O primeiro locator encontrado e visível.</returns>
    /// <exception cref="InvalidOperationException">Se nenhuma estratégia encontrar o elemento.</exception>
    public static async Task<ILocator> FindForFillAsync(IPage page, string hint)
    {
        var strategies = new (string Name, Func<ILocator> Fn)[]
        {
            ("GetByLabel",      () => page.GetByLabel(hint)),
            ("GetByPlaceholder",() => page.GetByPlaceholder(hint)),
            ("data-testid",     () => page.Locator($"[data-testid='{hint}']")),
            ("data-cy",         () => page.Locator($"[data-cy='{hint}']")),
            ("css/name",        () => page.Locator($"[name='{hint}']")),
            ("css",             () => page.Locator(hint)),
        };

        return await TryStrategiesAsync(hint, strategies)
               ?? throw new InvalidOperationException(
                   $"[PlaywrightElementHelper] Não foi possível encontrar o campo '{hint}'. " +
                   "Tentativas: GetByLabel, GetByPlaceholder, data-testid, data-cy, name attr, CSS selector.");
    }

    /// <summary>
    /// Localiza um elemento clicável (botão, link, qualquer elemento com texto).
    /// Tenta por: button role, link role, texto exacto, texto parcial, data-testid, data-cy, CSS selector.
    /// </summary>
    /// <param name="page">A página Playwright activa.</param>
    /// <param name="hint">Texto, data-testid, data-cy, ou CSS selector do elemento.</param>
    /// <returns>O primeiro locator encontrado e visível.</returns>
    /// <exception cref="InvalidOperationException">Se nenhuma estratégia encontrar o elemento.</exception>
    public static async Task<ILocator> FindForClickAsync(IPage page, string hint)
    {
        var strategies = new (string Name, Func<ILocator> Fn)[]
        {
            ("button[name]",    () => page.GetByRole(AriaRole.Button, new() { Name = hint })),
            ("link[name]",      () => page.GetByRole(AriaRole.Link, new() { Name = hint })),
            ("text[exact]",     () => page.GetByText(hint, new() { Exact = true })),
            ("text[partial]",   () => page.GetByText(hint, new() { Exact = false })),
            ("data-testid",     () => page.Locator($"[data-testid='{hint}']")),
            ("data-cy",         () => page.Locator($"[data-cy='{hint}']")),
            ("css",             () => page.Locator(hint)),
        };

        return await TryStrategiesAsync(hint, strategies)
               ?? throw new InvalidOperationException(
                   $"[PlaywrightElementHelper] Não foi possível encontrar o elemento '{hint}'. " +
                   "Tentativas: button, link, texto exacto, texto parcial, data-testid, data-cy, CSS selector.");
    }

    /// <summary>
    /// Verifica se um elemento está visível na página.
    /// Tenta por: data-testid, data-cy, texto exacto, CSS selector.
    /// </summary>
    /// <param name="page">A página Playwright activa.</param>
    /// <param name="hint">Texto visível, data-testid, data-cy, ou CSS selector.</param>
    /// <returns>True se o elemento estiver visível, false caso contrário.</returns>
    public static async Task<bool> IsVisibleAsync(IPage page, string hint)
    {
        var strategies = new (string Name, Func<ILocator> Fn)[]
        {
            ("text[exact]",   () => page.GetByText(hint, new() { Exact = true })),
            ("text[partial]", () => page.GetByText(hint, new() { Exact = false })),
            ("data-testid",   () => page.Locator($"[data-testid='{hint}']")),
            ("data-cy",       () => page.Locator($"[data-cy='{hint}']")),
            ("css",           () => page.Locator(hint)),
        };

        var locator = await TryStrategiesAsync(hint, strategies);
        return locator is not null;
    }

    /// <summary>
    /// Localiza um campo para ler o seu valor.
    /// Tenta por: label, placeholder, data-testid, data-cy, name attr, CSS selector.
    /// </summary>
    public static async Task<ILocator> FindForReadAsync(IPage page, string hint)
    {
        return await FindForFillAsync(page, hint);
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

                // Verifica rapidamente se existe pelo menos um elemento visível
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
                // Estratégia não encontrou o elemento — tenta a próxima
            }
        }

        return null;
    }
}

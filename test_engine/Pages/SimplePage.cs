using FunctionalTests.Config;

namespace FunctionalTests.Pages;

/// <summary>
/// Exemplo de Page Object genérico.
/// Representa uma página acessível diretamente pela BaseUrl.
/// Sistemas de IA podem clonar/estender este padrão para novas páginas.
/// </summary>
public class SimplePage : BasePage
{
    public SimplePage(IBrowser browser, IPage page)
    {
        Browser = browser;
        Page = page;
    }

    public override string PagePath => "";

    public override IBrowser Browser { get; }

    public override IPage Page { get; set; }

    public Task<string> GetTitleAsync() => Page.TitleAsync();
}


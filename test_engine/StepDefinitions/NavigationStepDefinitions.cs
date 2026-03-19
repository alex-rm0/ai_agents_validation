using FunctionalTests.Config;
using FunctionalTests.Pages;

namespace FunctionalTests.StepDefinitions;

/// <summary>
/// Step definitions genéricos para navegação.
/// Podem ser reutilizados por múltiplos .feature gerados automaticamente.
/// </summary>
[Binding]
public sealed class NavigationStepDefinitions
{
    private readonly IPage _page;
    private readonly IBrowser _browser;
    private SimplePage? _simplePage;

    public NavigationStepDefinitions(IPage page, IBrowser browser)
    {
        _page = page;
        _browser = browser;
    }

    /// <summary>
    /// Garante que a BASE_URL está definida (via env ou appsettings).
    /// </summary>
    [Given("the application base url is configured")]
    public void GivenTheApplicationBaseUrlIsConfigured()
    {
        TestConfig.BaseUrl.ShouldNotBeNullOrWhiteSpace();
    }

    /// <summary>
    /// Navega para a página inicial (BaseUrl).
    /// </summary>
    [When("I navigate to the home page")]
    public async Task WhenINavigateToTheHomePage()
    {
        _simplePage ??= new SimplePage(_browser, _page);
        await _simplePage.GotoAsync();
    }

    /// <summary>
    /// Verifica que o browser está na BaseUrl (ou prefixo).
    /// </summary>
    [Then("the browser should be at the base url")]
    public void ThenTheBrowserShouldBeAtTheBaseUrl()
    {
        var currentUrl = _page.Url;
        currentUrl.ShouldStartWith(TestConfig.BaseUrl);
    }
}


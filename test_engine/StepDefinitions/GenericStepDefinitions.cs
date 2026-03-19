using FunctionalTests.Config;
using FunctionalTests.Helpers;
using Microsoft.Playwright;
using Reqnroll;
using Shouldly;

namespace FunctionalTests.StepDefinitions;

/// <summary>
/// Biblioteca de step definitions genéricas com vocabulário controlado.
/// Todos os steps que interagem com o DOM usam PlaywrightElementHelper.FindElementAsync
/// com a estratégia: placeholder → label → texto visível → data-testid/data-cy → CSS selector.
///
/// Qualquer .feature em Features/generated/ que use exclusivamente este vocabulário
/// corre sem necessidade de implementação C# adicional.
///
/// Vocabulário completo: test_engine/docs/step-vocabulary.md
/// </summary>
[Binding]
public sealed class GenericStepDefinitions
{
    private readonly IPage _page;
    private readonly IBrowser _browser;
    private readonly IBrowserContext _context;

    public GenericStepDefinitions(IPage page, IBrowser browser, IBrowserContext context)
    {
        _page = page;
        _browser = browser;
        _context = context;
    }

    // ─── Given ───────────────────────────────────────────────────────────────

    /// <summary>
    /// Navega para uma rota relativa à BASE_URL.
    /// Exemplos: "login", "dashboard", "#/settings", "/", ou URL absoluta.
    /// </summary>
    [Given(@"the user navigates to ""(.+)""")]
    public async Task GivenTheUserNavigatesTo(string route)
    {
        var baseUrl = TestConfig.BaseUrl;
        var url = route.StartsWith("http", StringComparison.OrdinalIgnoreCase)
            ? route
            : $"{baseUrl.TrimEnd('/')}/{route.TrimStart('/')}";

        Console.WriteLine($"[GenericSteps] A navegar para: {url}");

        await _page.GotoAsync(url, new PageGotoOptions
        {
            WaitUntil = WaitUntilState.DOMContentLoaded,
            Timeout = 30_000,
        });
    }

    /// <summary>
    /// Realiza login com as credenciais configuradas em TestConfig / appsettings.json.
    /// Navega para LoginPath, preenche username/password usando os selectores configurados,
    /// e aguarda que a URL mude (indica autenticação). Não lança excepção em caso de timeout —
    /// as asserções seguintes verificarão se o login foi bem-sucedido.
    /// </summary>
    [Given(@"the user is logged in")]
    public async Task GivenTheUserIsLoggedIn()
    {
        var loginUrl = $"{TestConfig.BaseUrl.TrimEnd('/')}/{TestConfig.LoginPath.TrimStart('/')}";
        Console.WriteLine($"[GenericSteps] Login automático — a navegar para: {loginUrl}");

        await _page.GotoAsync(loginUrl, new PageGotoOptions
        {
            WaitUntil = WaitUntilState.DOMContentLoaded,
            Timeout = 30_000,
        });

        // Localiza os elementos de login via PlaywrightElementHelper (usa selectores de TestConfig como hints)
        var usernameEl = await PlaywrightElementHelper.FindElementAsync(_page, TestConfig.UsernameSelector);
        await usernameEl.FillAsync(TestConfig.TestUser);

        var passwordEl = await PlaywrightElementHelper.FindElementAsync(_page, TestConfig.PasswordSelector);
        await passwordEl.FillAsync(TestConfig.TestPassword);

        var loginBtn = await PlaywrightElementHelper.FindElementAsync(_page, TestConfig.LoginButtonSelector);
        await loginBtn.ClickAsync();

        // Aguarda que a URL mude — se não mudar, as asserções seguintes irão detectar o falhanço.
        try
        {
            await _page.WaitForURLAsync(
                url => !url.Contains(TestConfig.LoginPath, StringComparison.OrdinalIgnoreCase),
                new PageWaitForURLOptions { Timeout = 15_000 }
            );
            Console.WriteLine($"[GenericSteps] Login concluído. URL actual: {_page.Url}");
        }
        catch (TimeoutException)
        {
            Console.WriteLine($"[GenericSteps] Login timeout — URL ainda é: {_page.Url}. " +
                              "As verificações seguintes irão detectar o falhanço.");
        }
    }

    // ─── When ────────────────────────────────────────────────────────────────

    /// <summary>
    /// Preenche um campo de formulário com um valor.
    /// O campo é identificado por PlaywrightElementHelper (placeholder → label → texto → data-testid → CSS).
    /// </summary>
    [When(@"the user fills ""(.+)"" with ""(.*)""")]
    public async Task WhenTheUserFillsFieldWith(string field, string value)
    {
        Console.WriteLine($"[GenericSteps] Preencher '{field}' com '{value}'");
        var element = await PlaywrightElementHelper.FindElementAsync(_page, field);
        await element.FillAsync(value);
    }

    /// <summary>
    /// Limpa o conteúdo de um campo de formulário.
    /// O campo é identificado por PlaywrightElementHelper (placeholder → label → texto → data-testid → CSS).
    /// </summary>
    [When(@"the user clears ""(.+)""")]
    public async Task WhenTheUserClearsField(string field)
    {
        Console.WriteLine($"[GenericSteps] Limpar campo '{field}'");
        var element = await PlaywrightElementHelper.FindElementAsync(_page, field);
        await element.ClearAsync();
    }

    /// <summary>
    /// Clica num elemento (botão, link, checkbox, tab, etc.).
    /// O elemento é identificado por PlaywrightElementHelper (placeholder → label → texto → data-testid → CSS).
    /// </summary>
    [When(@"the user clicks ""(.+)""")]
    public async Task WhenTheUserClicksElement(string element)
    {
        Console.WriteLine($"[GenericSteps] Clicar em '{element}'");
        var locator = await PlaywrightElementHelper.FindElementAsync(_page, element);
        await locator.ClickAsync();
    }

    /// <summary>
    /// Submete o formulário activo.
    /// Localiza o botão de submit via PlaywrightElementHelper usando o selector CSS padrão.
    /// </summary>
    [When(@"the user submits the form")]
    public async Task WhenTheUserSubmitsTheForm()
    {
        Console.WriteLine("[GenericSteps] Submeter formulário");
        var submitButton = await PlaywrightElementHelper.FindElementAsync(
            _page, "button[type='submit'], input[type='submit']");
        await submitButton.ClickAsync();
    }

    /// <summary>
    /// Aguarda N segundos (útil para animações ou carregamentos lentos).
    /// </summary>
    [When(@"the user waits (\d+) seconds?")]
    public async Task WhenTheUserWaitsSeconds(int seconds)
    {
        Console.WriteLine($"[GenericSteps] A aguardar {seconds} segundo(s)");
        await Task.Delay(TimeSpan.FromSeconds(seconds));
    }

    // ─── Then ────────────────────────────────────────────────────────────────

    /// <summary>
    /// Verifica que um texto está visível na página.
    /// Usa PlaywrightElementHelper para localizar o texto com a estratégia padrão.
    /// </summary>
    [Then(@"the user should see ""(.+)""")]
    public async Task ThenTheUserShouldSee(string text)
    {
        Console.WriteLine($"[GenericSteps] Verificar texto visível: '{text}'");
        var isVisible = await PlaywrightElementHelper.IsElementVisibleAsync(_page, text);
        isVisible.ShouldBeTrue($"Esperava ver o texto '{text}' na página, mas não foi encontrado.");
    }

    /// <summary>
    /// Verifica que um texto NÃO está visível na página.
    /// Usa PlaywrightElementHelper para confirmar ausência do elemento.
    /// </summary>
    [Then(@"the user should not see ""(.+)""")]
    public async Task ThenTheUserShouldNotSee(string text)
    {
        Console.WriteLine($"[GenericSteps] Verificar texto ausente: '{text}'");

        // Pequena espera para garantir que o texto não aparece após animações
        await Task.Delay(500);

        var isVisible = await PlaywrightElementHelper.IsElementVisibleAsync(_page, text);
        isVisible.ShouldBeFalse($"O texto '{text}' está visível na página mas não deveria estar.");
    }

    /// <summary>
    /// Verifica que a URL actual contém um fragmento específico.
    /// Aguarda que a URL mude (WaitForURLAsync) e depois asserta.
    /// </summary>
    [Then(@"the url should contain ""(.+)""")]
    public async Task ThenTheUrlShouldContain(string fragment)
    {
        Console.WriteLine($"[GenericSteps] Verificar URL contém: '{fragment}'");

        await _page.WaitForURLAsync(
            url => url.Contains(fragment, StringComparison.OrdinalIgnoreCase),
            new PageWaitForURLOptions { Timeout = 10_000 }
        );

        _page.Url.Contains(fragment, StringComparison.OrdinalIgnoreCase)
            .ShouldBeTrue($"Esperava que a URL contivesse '{fragment}', mas a URL actual é '{_page.Url}'.");
    }

    /// <summary>
    /// Verifica que a URL actual é exactamente a URL especificada.
    /// </summary>
    [Then(@"the url should be ""(.+)""")]
    public async Task ThenTheUrlShouldBe(string expectedUrl)
    {
        Console.WriteLine($"[GenericSteps] Verificar URL exacta: '{expectedUrl}'");

        await _page.WaitForURLAsync(expectedUrl, new PageWaitForURLOptions { Timeout = 10_000 });

        _page.Url.ShouldBe(expectedUrl,
            $"Esperava que a URL fosse '{expectedUrl}', mas a URL actual é '{_page.Url}'.");
    }

    /// <summary>
    /// Verifica que um elemento (identificado por CSS selector, data-testid, data-cy, ou texto) está visível.
    /// Usa PlaywrightElementHelper com a estratégia padrão.
    /// </summary>
    [Then(@"the element ""(.+)"" should be visible")]
    public async Task ThenElementShouldBeVisible(string selector)
    {
        Console.WriteLine($"[GenericSteps] Verificar elemento visível: '{selector}'");
        var isVisible = await PlaywrightElementHelper.IsElementVisibleAsync(_page, selector);
        isVisible.ShouldBeTrue($"O elemento '{selector}' deveria estar visível mas não está.");
    }

    /// <summary>
    /// Verifica que um elemento (identificado por CSS selector, data-testid, data-cy, ou texto) NÃO está visível.
    /// Usa PlaywrightElementHelper com a estratégia padrão.
    /// </summary>
    [Then(@"the element ""(.+)"" should not be visible")]
    public async Task ThenElementShouldNotBeVisible(string selector)
    {
        Console.WriteLine($"[GenericSteps] Verificar elemento oculto: '{selector}'");
        await Task.Delay(500);
        var isVisible = await PlaywrightElementHelper.IsElementVisibleAsync(_page, selector);
        isVisible.ShouldBeFalse($"O elemento '{selector}' deveria estar oculto mas está visível.");
    }

    /// <summary>
    /// Verifica que o valor de um campo de formulário contém o texto esperado.
    /// Usa PlaywrightElementHelper para localizar o campo.
    /// </summary>
    [Then(@"the field ""(.+)"" should contain ""(.*)""")]
    public async Task ThenTheFieldShouldContain(string field, string expectedValue)
    {
        Console.WriteLine($"[GenericSteps] Verificar campo '{field}' contém '{expectedValue}'");
        var element = await PlaywrightElementHelper.FindElementAsync(_page, field);
        var actualValue = await element.InputValueAsync();
        actualValue.Contains(expectedValue)
            .ShouldBeTrue($"O campo '{field}' deveria conter '{expectedValue}', mas contém '{actualValue}'.");
    }

    /// <summary>
    /// Verifica que o título da página (tag &lt;title&gt;) é o esperado.
    /// </summary>
    [Then(@"the page title should be ""(.+)""")]
    public async Task ThenThePageTitleShouldBe(string expectedTitle)
    {
        Console.WriteLine($"[GenericSteps] Verificar título da página: '{expectedTitle}'");
        var actualTitle = await _page.TitleAsync();
        actualTitle.ShouldBe(expectedTitle,
            $"O título da página deveria ser '{expectedTitle}', mas é '{actualTitle}'.");
    }
}

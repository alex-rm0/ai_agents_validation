using FunctionalTests.Helpers;
using FunctionalTests.Pages;
using Microsoft.Playwright;
using Reqnroll;
using Shouldly;

namespace FunctionalTests.StepDefinitions;

[Binding]
public sealed class LoginStepDefinitions
{
    private readonly IPage _page;
    private readonly IBrowser _browser;
    private readonly IBrowserContext _context;
    private readonly LoginPage _loginPage;

    public LoginStepDefinitions(IPage page, IBrowser browser, IBrowserContext context)
    {
        _page = page;
        _browser = browser;
        _context = context;
        _loginPage = new LoginPage(_browser, _context, _page);
    }

    [Given("a user is on the login page")]
    public async Task GivenAUserIsOnTheLoginPage()
    {
        await _loginPage.GotoAsync();

        Console.WriteLine($"[Step Given] URL após navegação: {_page.Url}");
        Console.WriteLine($"[Step Given] Page fechada? {_page.IsClosed}");
        Console.WriteLine($"[Step Given] Páginas no contexto: {_context.Pages.Count}");
    }

    [When("the user logs in with valid credentials")]
    public async Task WhenTheUserLogsInWithValidCredentials()
    {
        var username = ConfigurationHelper.GetTestUser();
        var password = ConfigurationHelper.GetTestPassword();

        Console.WriteLine($"[Step When] URL atual: {_page.Url}");
        Console.WriteLine($"[Step When] Page fechada? {_page.IsClosed}");
        Console.WriteLine($"[Step When] Páginas no contexto: {_context.Pages.Count}");

        await _loginPage.LoginAsync(username, password);
    }

    [Then("the user should be authenticated")]
    public async Task ThenTheUserShouldBeAuthenticated()
    {
        var authenticated = await _loginPage.IsAuthenticatedAsync();
        authenticated.ShouldBeTrue();
    }
}
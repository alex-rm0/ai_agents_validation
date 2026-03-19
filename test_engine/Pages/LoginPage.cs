using FunctionalTests.Helpers;
using Microsoft.Playwright;

namespace FunctionalTests.Pages;

public class LoginPage : BasePage
{
    private readonly IBrowserContext _context;

    public LoginPage(IBrowser browser, IBrowserContext context, IPage page)
    {
        Browser = browser;
        _context = context;
        Page = page;
    }

    public override string PagePath => ConfigurationHelper.GetLoginPath();

    public override IBrowser Browser { get; }

    public override IPage Page { get; set; }

    public async Task LoginAsync(string username, string password)
    {
        Console.WriteLine($"[LoginAsync] URL atual: {Page.Url}");
        Console.WriteLine($"[LoginAsync] Page fechada? {Page.IsClosed}");
        Console.WriteLine($"[LoginAsync] Número de páginas no contexto antes da espera: {_context.Pages.Count}");

        await Page.WaitForTimeoutAsync(2000);

        Console.WriteLine($"[LoginAsync] Número de páginas no contexto depois da espera: {_context.Pages.Count}");

        if (Page.IsClosed && _context.Pages.Count > 0)
        {
            Page = _context.Pages.Last();
            Console.WriteLine($"[LoginAsync] A usar nova página: {Page.Url}");
        }

        var usernameSelector = ConfigurationHelper.GetUsernameSelector();
        var passwordSelector = ConfigurationHelper.GetPasswordSelector();
        var loginButtonSelector = ConfigurationHelper.GetLoginButtonSelector();

        await Page.Locator(usernameSelector).WaitForAsync(new LocatorWaitForOptions
        {
            Timeout = 10000
        });

        await Page.Locator(usernameSelector).FillAsync(username);
        await Page.Locator(passwordSelector).WaitForAsync(new LocatorWaitForOptions
        {
            Timeout = 10000
        });
        await Page.Locator(passwordSelector).FillAsync(password);
        await Page.Locator(loginButtonSelector).ClickAsync();
    }

    public async Task<bool> IsAuthenticatedAsync()
    {
        try
        {
            await Page.WaitForURLAsync(
                url => !url.Contains("login", StringComparison.OrdinalIgnoreCase),
                new PageWaitForURLOptions { Timeout = 15000 }
            );
            Console.WriteLine($"[IsAuthenticatedAsync] URL após login: {Page.Url}");
            return true;
        }
        catch (TimeoutException)
        {
            Console.WriteLine($"[IsAuthenticatedAsync] Timeout — URL ainda é: {Page.Url}");
            return false;
        }
    }
}
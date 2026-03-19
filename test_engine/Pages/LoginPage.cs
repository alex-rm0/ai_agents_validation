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

        await Page.Locator("input[data-cy='email']").WaitForAsync(new LocatorWaitForOptions
        {
            Timeout = 10000
        });

        await Page.Locator("input[data-cy='email']").FillAsync(username);
        await Page.Locator("input[data-cy='password']").WaitForAsync(new LocatorWaitForOptions
        {
            Timeout = 10000
        });
        await Page.Locator("input[data-cy='password']").FillAsync(password);
        await Page.Locator("text=Iniciar Sessão").ClickAsync();
    }

    public async Task<bool> IsAuthenticatedAsync()
    {
        await Page.WaitForLoadStateAsync(LoadState.DOMContentLoaded);
        return !Page.Url.Contains("login", StringComparison.OrdinalIgnoreCase);
    }
}
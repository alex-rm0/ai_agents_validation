using FunctionalTests.Config;
using Microsoft.Playwright;
using Reqnroll;
using Reqnroll.BoDi;

namespace FunctionalTests.Hooks;

/// <summary>
/// Common test hooks for all features
/// Manages browser lifecycle and dependency injection setup
/// </summary>
[Binding]
public sealed class CommonHooks
{
    /// <summary>
    /// Initialize Playwright browser before each scenario
    /// Registers all necessary dependencies in the DI container
    /// </summary>
    [BeforeScenario(Order = 0)]
    public static async Task BeforeScenario(IObjectContainer container)
    {
        // Create Playwright instance
        var playwright = await Playwright.CreateAsync();

        // Configure browser options
        var options = new BrowserTypeLaunchOptions
        {
            Headless = TestConfig.Headless,
            SlowMo = 50
        };

        // Launch browser
        var browser = await playwright.Chromium.LaunchAsync(options);

        // Create browser context with default settings
        var context = await browser.NewContextAsync(new BrowserNewContextOptions
        {
            IgnoreHTTPSErrors = true,
            ViewportSize = new ViewportSize { Width = 1920, Height = 1080 },
            AcceptDownloads = true
        });

        context.Page += async (_, newPage) =>
        {
            Console.WriteLine($"[Playwright] NOVA PAGE DETETADA: {newPage.Url}");
            newPage.Close += (_, _) => Console.WriteLine("[Playwright] NEW PAGE CLOSED");
            newPage.Console += (_, msg) => Console.WriteLine($"[New Page Console] {msg.Text}");
            await Task.CompletedTask;
        };

        // Create page
        var page = await context.NewPageAsync();

        // Enable console logging for debugging
        page.Close += (_, _) => Console.WriteLine("[Playwright] PAGE CLOSED");
        context.Close += (_, _) => Console.WriteLine("[Playwright] CONTEXT CLOSED");
        browser.Disconnected += (_, _) => Console.WriteLine("[Playwright] BROWSER DISCONNECTED");
        page.Console += (_, msg) => Console.WriteLine($"[Browser Console] {msg.Text}");
        page.PageError += (_, exception) => Console.WriteLine($"[Browser Error] {exception}");

        // Register instances in DI container
        container.RegisterInstanceAs(playwright);
        container.RegisterInstanceAs(browser);
        container.RegisterInstanceAs(context);
        container.RegisterInstanceAs(page);
    }

    /// <summary>
    /// Cleanup after each scenario
    /// </summary>
    [AfterScenario(Order = 100)]
    public static async Task AfterScenario(IObjectContainer container)
    {
        try
        {
            // Resolve and cleanup in reverse order
            if (container.IsRegistered<IBrowserContext>())
            {
                var context = container.Resolve<IBrowserContext>();
                await context.CloseAsync();
            }

            if (container.IsRegistered<IBrowser>())
            {
                var browser = container.Resolve<IBrowser>();
                await browser.CloseAsync();
            }

            if (container.IsRegistered<IPlaywright>())
            {
                var playwright = container.Resolve<IPlaywright>();
                playwright.Dispose();
            }
        }
        catch (Exception ex)
        {
            Console.WriteLine($"[Cleanup Error] {ex.Message}");
        }
    }
}

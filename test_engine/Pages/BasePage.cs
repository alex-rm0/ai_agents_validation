/*
using FunctionalTests.Config;

namespace FunctionalTests.Pages;

/// <summary>
/// Page Object base genérico para páginas da aplicação.
/// </summary>
public abstract class BasePage
{
    protected static string BaseUrl => TestConfig.BaseUrl;

    public abstract string PagePath { get; }

    public abstract IBrowser Browser { get; }

    public abstract IPage Page { get; set; }

    public virtual Task GotoAsync() =>
        Page.GotoAsync(PagePath);
}
*/
using FunctionalTests.Helpers;
using Microsoft.Playwright;

namespace FunctionalTests.Pages;

public abstract class BasePage
{
    public abstract IBrowser Browser { get; }
    public abstract IPage Page { get; set; }
    public abstract string PagePath { get; }

    protected string BaseUrl => ConfigurationHelper.GetBaseUrl();

    public virtual async Task GotoAsync()
    {
        var url = string.IsNullOrWhiteSpace(PagePath)
            ? BaseUrl
            : $"{BaseUrl.TrimEnd('/')}/{PagePath.TrimStart('/')}";

        Console.WriteLine($"[BasePage.GotoAsync] A navegar para: {url}");
        Console.WriteLine($"[BasePage.GotoAsync] Page fechada antes do Goto? {Page.IsClosed}");

        await Page.GotoAsync(url, new PageGotoOptions
        {
            WaitUntil = WaitUntilState.DOMContentLoaded,
            Timeout = 30000
        });

        Console.WriteLine($"[BasePage.GotoAsync] URL atual após Goto: {Page.Url}");
        Console.WriteLine($"[BasePage.GotoAsync] Page fechada depois do Goto? {Page.IsClosed}");
    }
}
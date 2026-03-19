using Microsoft.Extensions.Configuration;

namespace FunctionalTests.Config;

/// <summary>
/// Configuração base dos testes funcionais.
/// Lê primeiro de variáveis de ambiente e depois de appsettings.json (via IConfiguration).
/// </summary>
public static class TestConfig
{
    private static readonly IConfiguration _configuration;

    static TestConfig()
    {
        _configuration = new ConfigurationBuilder()
            .AddJsonFile("appsettings.json", optional: true)
            .AddEnvironmentVariables()
            .Build();
    }

    /// <summary>
    /// URL base da aplicação sob teste.
    /// Env: BASE_URL
    /// </summary>
    public static string BaseUrl =>
        (Environment.GetEnvironmentVariable("BASE_URL")
         ?? _configuration["BaseUrl"]
         ?? "about:blank").TrimEnd('/');

    /// <summary>
    /// Indica se o browser deve correr em modo headless.
    /// Env: HEADLESS (true/false)
    /// </summary>
    public static bool Headless
    {
        get
        {
            var fromEnv = Environment.GetEnvironmentVariable("HEADLESS");
            if (!string.IsNullOrWhiteSpace(fromEnv))
            {
                return fromEnv.Trim().Equals("true", StringComparison.OrdinalIgnoreCase);
            }

            var fromConfig = _configuration["Headless"];
            if (!string.IsNullOrWhiteSpace(fromConfig))
            {
                return fromConfig.Trim().Equals("true", StringComparison.OrdinalIgnoreCase);
            }

            return true;
        }
    }

    /// <summary>
    /// Caminho de login (ex: #/login).
    /// Env: LOGIN_PATH
    /// </summary>
    public static string LoginPath =>
        Environment.GetEnvironmentVariable("LOGIN_PATH")
        ?? _configuration["LoginPath"]
        ?? "";

    /// <summary>
    /// Username de teste.
    /// Env: TEST_USER
    /// </summary>
    public static string TestUser =>
        Environment.GetEnvironmentVariable("TEST_USER")
        ?? _configuration["TestUser"]
        ?? throw new InvalidOperationException("TestUser is not configured.");

    /// <summary>
    /// Password de teste.
    /// Env: TEST_PASSWORD
    /// </summary>
    public static string TestPassword =>
        Environment.GetEnvironmentVariable("TEST_PASSWORD")
        ?? _configuration["TestPassword"]
        ?? throw new InvalidOperationException("TestPassword is not configured.");

    /// <summary>
    /// Selector do campo de username/email na página de login.
    /// Env: USERNAME_SELECTOR
    /// </summary>
    public static string UsernameSelector =>
        Environment.GetEnvironmentVariable("USERNAME_SELECTOR")
        ?? _configuration["UsernameSelector"]
        ?? "input[type='text']";

    /// <summary>
    /// Selector do campo de password na página de login.
    /// Env: PASSWORD_SELECTOR
    /// </summary>
    public static string PasswordSelector =>
        Environment.GetEnvironmentVariable("PASSWORD_SELECTOR")
        ?? _configuration["PasswordSelector"]
        ?? "input[type='password']";

    /// <summary>
    /// Selector do botão de login.
    /// Env: LOGIN_BUTTON_SELECTOR
    /// </summary>
    public static string LoginButtonSelector =>
        Environment.GetEnvironmentVariable("LOGIN_BUTTON_SELECTOR")
        ?? _configuration["LoginButtonSelector"]
        ?? "button[type='submit']";
}


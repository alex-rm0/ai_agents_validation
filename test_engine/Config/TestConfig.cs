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
}


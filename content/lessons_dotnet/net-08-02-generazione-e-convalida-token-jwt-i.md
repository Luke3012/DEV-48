# Generazione e convalida token JWT in ASP.NET Core

## In parole semplici

L'obiettivo di questa lezione è configurare la validazione JWT in ASP.NET Core, seguire in un esempio locale come viene emesso un token e applicare una policy di ruolo sugli endpoint Minimal API.

In un esempio didattico locale, ASP.NET Core può emettere un token dopo aver verificato credenziali dimostrative e convalidare firma, issuer, audience e scadenza sulle richieste successive. L'autenticazione stabilisce chi presenta il token; una policy decide quali ruoli possono usare un endpoint.

## Le parole da riconoscere

- `jwtsecuritytokenhandler`
- `symmetricsecuritykey`
- `requireauthorization`
- `dotnet user-secrets`
- `claimstype`
- `authorization policy`

## Anatomia e Sintassi del Codice

### Prepara la chiave locale in PowerShell
Esegui i comandi nella cartella che contiene `Server.csproj`; `dotnet user-secrets init` si esegue una sola volta per progetto. Il pacchetto abilita la convalida Bearer nell'API. User Secrets mantiene una chiave di sviluppo fuori dal repository; genera una chiave casuale sul tuo computer.

```powershell
dotnet add package Microsoft.AspNetCore.Authentication.JwtBearer --version 10.0.12
dotnet user-secrets init
$jwtKey = [Convert]::ToBase64String([System.Security.Cryptography.RandomNumberGenerator]::GetBytes(32))
dotnet user-secrets set "Jwt:SigningKey" $jwtKey
```

### Generazione, convalida e autorizzazione in `Program.cs`
```csharp
using System.IdentityModel.Tokens.Jwt;
using System.Security.Claims;
using System.Text;
using Microsoft.AspNetCore.Authentication.JwtBearer;
using Microsoft.IdentityModel.Tokens;

var builder = WebApplication.CreateBuilder(args);
var signingKey = builder.Configuration["Jwt:SigningKey"]
    ?? throw new InvalidOperationException("Configura Jwt:SigningKey per lo sviluppo.");
var key = new SymmetricSecurityKey(Encoding.UTF8.GetBytes(signingKey));
const string issuer = "dev48-local-demo";
const string audience = "dev48-local-client";

builder.Services.AddAuthentication(JwtBearerDefaults.AuthenticationScheme)
    .AddJwtBearer(options => options.TokenValidationParameters = new TokenValidationParameters
    {
        ValidateIssuer = true, ValidIssuer = issuer,
        ValidateAudience = true, ValidAudience = audience,
        ValidateIssuerSigningKey = true, IssuerSigningKey = key,
        ValidateLifetime = true,
        NameClaimType = ClaimTypes.Name,
        RoleClaimType = ClaimTypes.Role
    });
builder.Services.AddAuthorization(options =>
    options.AddPolicy("AdminOnly", policy => policy.RequireRole("Admin")));

var app = builder.Build();
app.UseAuthentication();
app.UseAuthorization();

IResult Login(LoginRequest credentials)
{
    string? role = null;
    if (credentials.UserName == "demo") role = "Reader";
    if (credentials.UserName == "admin") role = "Admin";
    if (credentials.Password != "demo" || role is null) return Results.Unauthorized();

    var claims = new[]
    {
        new Claim(ClaimTypes.Name, credentials.UserName),
        new Claim(ClaimTypes.Role, role)
    };
    var token = new JwtSecurityToken(issuer, audience, claims,
        expires: DateTime.UtcNow.AddMinutes(15),
        signingCredentials: new SigningCredentials(key, SecurityAlgorithms.HmacSha256));
    return Results.Ok(new LoginResponse(new JwtSecurityTokenHandler().WriteToken(token)));
}

app.MapPost("/api/login", Login); // pubblico: restituisce un token breve per le credenziali demo
app.MapGet("/api/profile", (ClaimsPrincipal user) => Results.Ok(new { name = user.Identity?.Name }))
    .RequireAuthorization();
app.MapGet("/api/admin", () => Results.Ok("Area amministrativa"))
    .RequireAuthorization("AdminOnly");
app.Run();

public record LoginRequest(string UserName, string Password);
public record LoginResponse(string Token);
public partial class Program { }
```

Il token demo usa una chiave HMAC condivisa. User Secrets è solo per sviluppo locale e non cifra i valori: non distribuire questa API. Le credenziali fisse e la firma didattica servono solo a seguire il flusso; per un'app reale usa un provider e flussi standard OAuth/OIDC. Consulta le guide Microsoft su [User Secrets](https://learn.microsoft.com/en-us/aspnet/core/security/app-secrets?view=aspnetcore-10.0) e [JWT bearer e flussi di autenticazione](https://learn.microsoft.com/en-us/aspnet/core/security/authentication/configure-jwt-bearer-authentication?view=aspnetcore-10.0).

## Un esempio concreto

```text
POST /api/login { "userName": "demo", "password": "demo" } -> 200 con token
GET /api/profile senza token -> 401
GET /api/profile con token Reader -> 200
GET /api/admin con token Reader -> 403
POST /api/login con userName `admin` e password `demo`, poi GET /api/admin -> 200
```

### Seguilo passo per passo

1. In PowerShell inizializza User Secrets e genera una chiave casuale locale; il provider la rende leggibile da `builder.Configuration` in ambiente Development.
2. `AddJwtBearer` convalida firma, issuer, audience e scadenza. `UseAuthentication()` deve precedere `UseAuthorization()` perché prima si costruisce l'identità e poi si applicano le policy.
3. La rotta `/api/login` verifica credenziali solo dimostrative, crea claim di nome e ruolo e firma un token breve. `RequireAuthorization()` richiede un utente autenticato; `AdminOnly` controlla anche il ruolo.
4. Prova `/api/profile` senza token (401), con token Reader (200), poi `/api/admin` con Reader (403) e con Admin (200). Non distribuire questo emettitore demo: usa OAuth/OIDC per applicazioni reali.

## Pattern Guida per gli Esercizi

La pratica breve isola una regola e non avvia l'applicazione .NET. Prova la consegna con gli aiuti chiusi e usa l’esempio della lezione per ricostruire i passaggi che ti mancano. Nel laboratorio del modulo verifica anche il comportamento del framework.

## Dove ci si confonde spesso

- Usare questa rotta demo come sistema di login reale
- salvare chiavi o token nel repository
- confondere `RequireAuthorization()` (serve un utente autenticato) con una policy di ruolo
- fidarsi di una guard Angular al posto della policy API.

## Domanda di verifica

> Che differenza c'è tra `RequireAuthorization()` e `RequireAuthorization("AdminOnly")` e quali risposte HTTP ti aspetti?

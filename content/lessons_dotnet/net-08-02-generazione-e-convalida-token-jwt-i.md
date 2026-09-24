# Generazione e convalida token JWT in ASP.NET Core

## In parole semplici

L'obiettivo di questa lezione è configurare la validazione JWT in ASP.NET Core, seguire in un esempio locale come viene emesso un token e applicare una policy di ruolo sugli endpoint Minimal API.

In un esempio didattico locale, ASP.NET Core può emettere un token dopo aver verificato credenziali dimostrative e convalidare firma, issuer, audience e scadenza sulle richieste successive. L'autenticazione stabilisce chi presenta il token; una policy decide quali ruoli possono usare un endpoint.

### Prima di iniziare

Non dare per scontato di conoscere i termini elencati sotto: la spiegazione li introduce nel contesto. Se un termine resta poco chiaro, consulta il glossario e torna all'esempio.

## Le parole da riconoscere

- `jwtsecuritytokenhandler`
- `symmetricsecuritykey`
- `requireauthorization`
- `dotnet user-secrets`
- `claimstype`
- `authorization policy`

Non serve imparare questi termini a memoria. Concentrati inizialmente su **`jwtsecuritytokenhandler`, `symmetricsecuritykey`** e cerca di osservarli all'interno del codice e degli esercizi pratici.

## Anatomia e Sintassi del Codice

Leggi la spiegazione prima del codice. Quando compare una parola nuova, cerca il suo ruolo qui e prova a riconoscerla nell'esempio.

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

Questo è un esempio o un estratto minimo. Potrebbe dipendere da import, classi o configurazioni dichiarate altrove; il blocco mostra la parte pertinente al concetto.

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

La traccia seguente mostra un modo di applicare il concetto. Confrontala con il prompt e adatta i passaggi ai casi richiesti; potrebbe mostrare soltanto la parte centrale:

```csharp
public static class AuthClaimHelper {
    public static string ExtractUsername(string? emailClaim) =>
        string.IsNullOrWhiteSpace(emailClaim) ? "Guest" : emailClaim.Split('@')[0];
}
```

Prima di iniziare, prova a indicare che cosa ricevi, quale risultato ti aspetti e un caso limite. Poi affronta un passaggio alla volta e usa i controlli disponibili per verificare la consegna.

## Dove ci si confonde spesso

- Usare questa rotta demo come sistema di login reale
- salvare chiavi o token nel repository
- confondere `RequireAuthorization()` (serve un utente autenticato) con una policy di ruolo
- fidarsi di una guard Angular al posto della policy API.

Se qualcosa non funziona al primo tentativo, leggi il primo errore del compilatore o del test. Controlla una cosa alla volta: sintassi, tipo restituito, poi caso limite.

## Controllo rapido

- Riesco a spiegare il concetto principale con parole mie senza leggere?
- So identificare input, output e almeno un caso limite o di errore?
- Saprei applicare questa feature all'interno di un componente o di un'API reale?

## Domanda di verifica

> Che differenza c'è tra `RequireAuthorization()` e `RequireAuthorization("AdminOnly")` e quali risposte HTTP ti aspetti?

Prova a formulare una risposta chiara: prima definisci la regola generale, poi porta un esempio pratico, e infine cita un errore comune da evitare.

## Prima di andare avanti

Se una parte rimane poco chiara, torna al primo passaggio e spiega che cosa entra e che cosa esce dal codice. Passa all'esercizio quando riesci a prevedere almeno il caso normale e un caso limite.

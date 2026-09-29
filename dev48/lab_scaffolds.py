from __future__ import annotations

from html import escape
from pathlib import Path
import json
import shutil

from .models import Lab


ANGULAR_VERSION = "22.2.0"
TEST_SDK_VERSION = "17.14.1"
XUNIT_VERSION = "2.9.3"
XUNIT_RUNNER_VERSION = "3.1.5"


def course_lab_notes(lab: Lab) -> str:
    """Study instructions for new workspaces; never replace learner files."""
    steps = {
        "lab-net-csharp-crud": "Completa prima Search, poi Add, Update e Remove in SubjectCatalog.cs. Esegui un test alla volta e prova anche lista vuota e ID assente. I test xUnit sono già forniti: puoi leggerli qui prima della lezione dedicata; scriverne di nuovi sarà il passo successivo.",
        "lab-ts-angular-models": "Apri i modelli dell'ordine e segui ogni variante fino alla funzione di riepilogo. Correggi il caso cancelled senza ricorrere ad any. Esegui anche `npx tsc --noEmit -p tsconfig.app.json`: il runner breve delle lezioni non controlla questi tipi.",
        "lab-aspnet-minimal-api": "Segui una POST da Program.cs a SubjectStore e alla risposta 201. Lo starter contiene già rotte e DTO: completa la logica mancante, poi aggiungi un caso limite a Tests/LabTests.cs. Prova la stessa richiesta contro il server avviato.",
        "lab-angular-standalone": "Completa il filtro di visibleProducts in src/app/app.ts, poi verifica il template in src/app/app.html. Prova query senza risultati e selezione tramite pulsante. Aggiungi un test DOM: il filtro TypeScript corretto da solo non verifica i collegamenti del template.",
        "lab-angular-signals-state": "Correggi il totale che conta le righe invece di sommare i valori. Deriva gli altri indicatori con computed e prova aggiunta, rimozione e lista vuota. Usa effect soltanto per un effetto esterno, se necessario: i totali sono dati derivati.",
        "lab-efcore-sqlite-db": "Completa FindWithMeasuresAsync nel repository e verifica la relazione usando il database SQLite isolato dei test. Il test con EnsureCreated controlla il modello, ma non esegue le migrazioni. Per la migrazione, dalla cartella server esegui `dotnet tool restore`, `dotnet ef migrations add InitialSubjects`, poi `dotnet ef database update`. Non usare EnsureCreated sul database gestito dalle migrazioni.",
        "lab-angular-reactive-forms": "Completa il validatore remoto simulato e controlla invalid, pending e valid nel form reale. La disponibilità è simulata: il laboratorio non chiama un servizio esterno. Prova i messaggi vicino ai campi e l'invio da tastiera, oltre ai test automatici.",
        "lab-angular-routing-guard": "Completa la guard e verifica utente anonimo, ruolo errato e ruolo ammesso. Poi naviga tra le pagine dal browser: testare la funzione isolata non prova tutti i collegamenti. L'autorizzazione della risorsa deve comunque essere applicata nell'API.",
        "lab-fullstack-jwt-auth": "Il backend fornisce validazione e policy, ma la rotta login restituisce ancora 501 per le credenziali valide. Completa la generazione del token in Program.cs usando la lezione JWT, poi l'interceptor del client. Dalla cartella server configura la chiave con User Secrets come nella lezione JWT, avvia il server e ottieni un token demo. Imposta la sessione nel client e controlla l'header nel browser. I test backend verificano 401/403/200; quelli Angular usano un backend HTTP di test e non eseguono il login tra i due processi.",
        "lab-testing-xunit-vitest": "Completa la regola C# e la modifica di stato del componente. Prima osserva i test falliti, poi esegui le due suite separatamente. Aggiungi un caso limite per la regola e un'interazione DOM; modifica temporaneamente la logica per verificare che i tuoi test rilevino il difetto.",
        "lab-fullstack-monorepo-crud": "Completa la GET in SubjectsService e segui i dati fino alla lista. Le API e i metodi di scrittura del servizio sono forniti; aggiungi tu form e azioni UI per creare, modificare e rimuovere. Prova un ciclo completo dal browser e aggiungi test di loading, errore e lista vuota: i test iniziali non coprono l'intero CRUD dalla UI.",
        "lab-portfolio-enterprise": "Parti dalla base del gestionale e scegli una funzionalità piccola da completare in autonomia. Separa responsabilità dove il cambiamento lo richiede, aggiungi OpenAPI al backend e documenta comandi e decisioni. Lo starter non fornisce già tutti i layer o l'autorizzazione: applicali ai requisiti della tua funzionalità e verifica un caso di accesso negato quando ci sono risorse protette.",
    }
    if lab.id not in steps:
        return ""
    return "\n## Come affrontare questo laboratorio\n\n" + steps[lab.id] + "\n"


def ensure_course_scaffold(workspace: Path, lab: Lab) -> None:
    """Create genuine .NET and Angular workspaces for the corresponding lab."""
    _preserve_legacy_mock(workspace)
    if lab.workspace_template in {"dotnet", "monorepo"}:
        _ensure_dotnet_project(workspace / "server", lab)
    if lab.workspace_template in {"angular", "monorepo"}:
        _ensure_angular_project(workspace / "client", lab)


def _preserve_legacy_mock(workspace: Path) -> None:
    """Archive the old simulated starter before creating real CLI projects."""
    client = workspace / "client"
    marker = client / "src" / "app.component.js"
    package = client / "package.json"
    is_mock_client = marker.is_file() and "Angular Standalone Component simulato" in marker.read_text(encoding="utf-8", errors="replace")
    if package.is_file():
        package_text = package.read_text(encoding="utf-8", errors="replace")
        try:
            dependencies = json.loads(package_text).get("dependencies", {}) | json.loads(package_text).get("devDependencies", {})
        except (ValueError, TypeError):
            dependencies = {}
        is_mock_client = is_mock_client or ("vite" in dependencies and "@angular/cli" not in dependencies)
    if is_mock_client:
        _move_legacy(client, workspace / "client-legacy")

    server = workspace / "server"
    project = server / "Server.csproj"
    program = server / "Program.cs"
    if project.is_file() and program.is_file():
        project_text = project.read_text(encoding="utf-8", errors="replace")
        program_text = program.read_text(encoding="utf-8", errors="replace")
        if "<TargetFramework>net8.0</TargetFramework>" in project_text:
            _move_legacy(server, workspace / "server-legacy")


def _move_legacy(source: Path, destination: Path) -> None:
    candidate = destination
    suffix = 2
    while candidate.exists():
        candidate = destination.with_name(f"{destination.name}-{suffix}")
        suffix += 1
    shutil.move(str(source), str(candidate))


def _write_missing(root: Path, files: dict[str, str]) -> None:
    for relative, content in files.items():
        path = root / relative
        if path.exists():
            continue
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")


def _ensure_dotnet_project(server: Path, lab: Lab) -> None:
    api_labs = {
        "lab-aspnet-minimal-api",
        "lab-fullstack-jwt-auth",
        "lab-testing-xunit-vitest",
        "lab-fullstack-monorepo-crud",
        "lab-portfolio-enterprise",
    }
    ef_lab = lab.id == "lab-efcore-sqlite-db"
    pure_csharp_lab = lab.id == "lab-net-csharp-crud"
    testing_lab = lab.id == "lab-testing-xunit-vitest"
    project_sdk = "Microsoft.NET.Sdk" if pure_csharp_lab or testing_lab else "Microsoft.NET.Sdk.Web"
    project_type = "" if pure_csharp_lab or testing_lab else "<OutputType>Exe</OutputType>"
    additional_packages = ""
    if ef_lab:
        additional_packages += '    <PackageReference Include="Microsoft.EntityFrameworkCore.Sqlite" Version="10.0.12" />\n'
        additional_packages += '    <PackageReference Include="Microsoft.EntityFrameworkCore.Design" Version="10.0.12"><PrivateAssets>all</PrivateAssets></PackageReference>\n'
    if lab.id == "lab-fullstack-jwt-auth":
        additional_packages += '    <PackageReference Include="Microsoft.AspNetCore.Authentication.JwtBearer" Version="10.0.12" />\n'

    server_csproj = f'''<Project Sdk="{project_sdk}">
  <PropertyGroup>
    {project_type}
    <TargetFramework>net10.0</TargetFramework>
    <ImplicitUsings>enable</ImplicitUsings>
    <Nullable>enable</Nullable>
  </PropertyGroup>
  <ItemGroup>
{additional_packages.rstrip()}
  </ItemGroup>
  <ItemGroup>
    <Compile Remove="Tests/**/*.cs" />
  </ItemGroup>
</Project>
'''

    source_files: dict[str, str]
    test_source: str
    if pure_csharp_lab:
        source_files = {"SubjectCatalog.cs": '''namespace Dev48Lab;

public record Subject(int Id, string Name, string Zone, bool Active);

public sealed class SubjectCatalog
{
    private readonly List<Subject> _subjects = [];

    public IReadOnlyList<Subject> GetActive() => _subjects.Where(subject => subject.Active).ToArray();

    public IReadOnlyList<Subject> SearchByName(string? fragment)
    {
        if (string.IsNullOrWhiteSpace(fragment)) return [];
        // TODO: cerca senza distinguere maiuscole/minuscole e non esporre la lista interna.
        return [];
    }

    public Subject Add(string name, string zone, bool active = true)
    {
        if (string.IsNullOrWhiteSpace(name)) throw new ArgumentException("Il nome è obbligatorio.", nameof(name));
        // TODO: assegna un ID maggiore dei precedenti, pulisci i testi e aggiungi il record.
        throw new NotImplementedException("Completa Add.");
    }

    public bool Update(int id, string name, string zone)
    {
        if (string.IsNullOrWhiteSpace(name)) throw new ArgumentException("Il nome è obbligatorio.", nameof(name));
        // TODO: sostituisci il record trovato senza cambiare il suo ID o lo stato Active.
        return false;
    }

    public bool Remove(int id) => false; // TODO: rimuovi solo se trovi l'ID.
}
'''}
        test_source = '''using Dev48Lab;

namespace Dev48Lab.Tests;

public class SubjectCatalogTests
{
    [Fact]
    public void AddTrimsTheNameAndAssignsAnId()
    {
        var catalog = new SubjectCatalog();
        var added = catalog.Add("  Mario Rossi  ", " Centro ");
        Assert.Equal(1, added.Id);
        Assert.Equal("Mario Rossi", added.Name);
        Assert.Equal("Centro", added.Zone);
    }

    [Fact]
    public void EmptyNameIsRejected()
    {
        var catalog = new SubjectCatalog();
        Assert.Throws<ArgumentException>(() => catalog.Add("  ", "Centro"));
    }

    [Fact]
    public void RemoveReturnsFalseForAnUnknownId()
    {
        Assert.False(new SubjectCatalog().Remove(999));
    }

    [Fact]
    public void RemoveReturnsTrueForAnExistingId()
    {
        var catalog = new SubjectCatalog();
        var added = catalog.Add("Mario", "Centro");
        Assert.True(catalog.Remove(added.Id));
        Assert.Empty(catalog.GetActive());
    }

    [Fact]
    public void SearchByNameIgnoresCaseAndDoesNotMatchBlankText()
    {
        var catalog = new SubjectCatalog();
        catalog.Add("Mario Rossi", "Centro");
        Assert.Equal("Mario Rossi", Assert.Single(catalog.SearchByName(" MARIO ")).Name);
        Assert.Empty(catalog.SearchByName("  "));
    }

    [Fact]
    public void UpdateChangesTextAndKeepsTheId()
    {
        var catalog = new SubjectCatalog();
        var added = catalog.Add("Mario Rossi", "Centro", active: false);
        Assert.True(catalog.Update(added.Id, "  Mario R. ", " Nord "));
        var updated = Assert.Single(catalog.SearchByName("Mario R."));
        Assert.Equal(added.Id, updated.Id);
        Assert.Equal("Nord", updated.Zone);
        Assert.False(updated.Active);
    }

    [Fact]
    public void UpdateReturnsFalseForAnUnknownId()
    {
        var catalog = new SubjectCatalog();
        Assert.False(catalog.Update(999, "Mario", "Centro"));
    }

    [Fact]
    public void GetActiveExcludesInactiveSubjects()
    {
        var catalog = new SubjectCatalog();
        Assert.Empty(catalog.GetActive());
        catalog.Add("Attivo", "Nord");
        catalog.Add("Inattivo", "Sud", active: false);
        Assert.Equal("Attivo", Assert.Single(catalog.GetActive()).Name);
    }
}
'''
    elif testing_lab:
        source_files = {"SubjectRules.cs": '''namespace Dev48Lab;

public static class SubjectRules
{
    public static string? NormalizeName(string? name) => name; // TODO: rimuovi gli spazi e restituisci null se vuoto.
}
'''}
        test_source = '''using Dev48Lab;

namespace Dev48Lab.Tests;

public class SubjectRulesTests
{
    [Theory]
    [InlineData("  Mario Rossi  ", "Mario Rossi")]
    [InlineData("", null)]
    [InlineData("   ", null)]
    public void NormalizeNameTrimsTextAndRejectsBlankValues(string input, string? expected)
    {
        Assert.Equal(expected, SubjectRules.NormalizeName(input));
    }

    [Fact]
    public void NullNameStaysInvalid()
    {
        Assert.Null(SubjectRules.NormalizeName(null));
    }
}
'''
    elif ef_lab:
        source_files = {
            "Program.cs": '''using Dev48Lab;
using Microsoft.EntityFrameworkCore;

var builder = WebApplication.CreateBuilder(args);
var connectionString = builder.Configuration.GetConnectionString("Subjects") ?? "Data Source=subjects.db";
builder.Services.AddDbContext<AppDbContext>(options => options.UseSqlite(connectionString));
var app = builder.Build();

app.MapGet("/api/subjects", async (AppDbContext db, CancellationToken ct) =>
    await db.Subjects.AsNoTracking().ToListAsync(ct));
app.Run();

public partial class Program { }
''',
            "AppDbContext.cs": '''using Microsoft.EntityFrameworkCore;

namespace Dev48Lab;

public sealed class AppDbContext(DbContextOptions<AppDbContext> options) : DbContext(options)
{
    public DbSet<Subject> Subjects => Set<Subject>();
    public DbSet<Measure> Measures => Set<Measure>();

    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        modelBuilder.Entity<Subject>().HasMany(subject => subject.Measures).WithOne(measure => measure.Subject)
            .HasForeignKey(measure => measure.SubjectId);
    }
}

public sealed class Subject
{
    public int Id { get; set; }
    public string Name { get; set; } = "";
    public List<Measure> Measures { get; set; } = [];
}

public sealed class Measure
{
    public int Id { get; set; }
    public string Description { get; set; } = "";
    public int SubjectId { get; set; }
    public Subject Subject { get; set; } = null!;
}
''',
            "SubjectRepository.cs": '''using Microsoft.EntityFrameworkCore;

namespace Dev48Lab;

public sealed class SubjectRepository(AppDbContext db)
{
    public Task<Subject?> FindWithMeasuresAsync(int id, CancellationToken cancellationToken = default)
    {
        // TODO: carica il soggetto richiesto includendo le misure correlate.
        return Task.FromResult<Subject?>(null);
    }
}
''',
        }
        test_source = '''using Dev48Lab;
using Microsoft.Data.Sqlite;
using Microsoft.EntityFrameworkCore;

namespace Dev48Lab.Tests;

public class AppDbContextTests
{
    [Fact]
    public async Task SavesAndLoadsSubjectWithRelatedMeasures()
    {
        await using var connection = new SqliteConnection("Data Source=:memory:");
        await connection.OpenAsync();
        var options = new DbContextOptionsBuilder<AppDbContext>().UseSqlite(connection).Options;
        await using var db = new AppDbContext(options);
        await db.Database.EnsureCreatedAsync();
        var subject = new Subject { Name = "Mario" };
        subject.Measures.Add(new Measure { Description = "Verifica" });
        db.Subjects.Add(subject);
        await db.SaveChangesAsync();

        var saved = await new SubjectRepository(db).FindWithMeasuresAsync(subject.Id);
        Assert.NotNull(saved);
        Assert.Equal("Mario", saved.Name);
        Assert.Equal("Verifica", Assert.Single(saved.Measures).Description);
    }
}
'''
    elif lab.id == "lab-fullstack-jwt-auth":
        source_files = _jwt_api_files()
        test_source = '''using System.Net;
using System.Net.Http.Headers;
using System.Net.Http.Json;
using Dev48Lab;
using Microsoft.AspNetCore.Mvc.Testing;

namespace Dev48Lab.Tests;

public class JwtApiTests : IClassFixture<WebApplicationFactory<Program>>
{
    private readonly HttpClient _client;
    public JwtApiTests(WebApplicationFactory<Program> factory)
    {
        var previousSigningKey = Environment.GetEnvironmentVariable("Jwt__SigningKey");
        Environment.SetEnvironmentVariable("Jwt__SigningKey", "test-only-key-at-least-32-characters-long");
        try { _client = factory.CreateClient(); }
        finally { Environment.SetEnvironmentVariable("Jwt__SigningKey", previousSigningKey); }
    }

    [Fact]
    public async Task ProtectedRouteRejectsMissingToken()
    {
        var response = await _client.GetAsync("/api/profile");
        Assert.Equal(HttpStatusCode.Unauthorized, response.StatusCode);
    }

    [Fact]
    public async Task LoginRejectsWrongPassword()
    {
        var response = await _client.PostAsJsonAsync("/api/login", new LoginRequest("demo", "wrong"));
        Assert.Equal(HttpStatusCode.Unauthorized, response.StatusCode);
    }

    [Fact]
    public async Task ReaderTokenOpensProfile()
    {
        var token = await LoginAndGetToken("demo");
        _client.DefaultRequestHeaders.Authorization = new AuthenticationHeaderValue("Bearer", token);

        var response = await _client.GetAsync("/api/profile");
        Assert.Equal(HttpStatusCode.OK, response.StatusCode);
    }

    [Fact]
    public async Task ReaderTokenCannotOpenAdminRoute()
    {
        var token = await LoginAndGetToken("demo");
        _client.DefaultRequestHeaders.Authorization = new AuthenticationHeaderValue("Bearer", token);

        var response = await _client.GetAsync("/api/admin");
        Assert.Equal(HttpStatusCode.Forbidden, response.StatusCode);
    }

    [Fact]
    public async Task AdminTokenOpensAdminRoute()
    {
        var token = await LoginAndGetToken("admin");
        _client.DefaultRequestHeaders.Authorization = new AuthenticationHeaderValue("Bearer", token);

        var response = await _client.GetAsync("/api/admin");
        Assert.Equal(HttpStatusCode.OK, response.StatusCode);
    }

    private async Task<string> LoginAndGetToken(string userName)
    {
        var login = await _client.PostAsJsonAsync("/api/login", new LoginRequest(userName, "demo"));
        login.EnsureSuccessStatusCode();
        return (await login.Content.ReadFromJsonAsync<LoginResponse>())!.Token;
    }
}
'''
    else:
        source_files = _subjects_api_files(lab)
        test_source = '''using System.Net;
using System.Net.Http.Json;
using Microsoft.AspNetCore.Mvc.Testing;

namespace Dev48Lab.Tests;

public class SubjectsApiTests : IClassFixture<WebApplicationFactory<Program>>
{
    private readonly HttpClient _client;
    public SubjectsApiTests(WebApplicationFactory<Program> factory) => _client = factory.CreateClient();

    [Fact]
    public async Task ListReturnsSeedData()
    {
        var response = await _client.GetAsync("/api/subjects");
        Assert.Equal(HttpStatusCode.OK, response.StatusCode);
        var items = await response.Content.ReadFromJsonAsync<Subject[]>();
        Assert.NotEmpty(items!);
    }

    [Fact]
    public async Task CreateRejectsAnEmptyName()
    {
        var response = await _client.PostAsJsonAsync("/api/subjects", new CreateSubjectRequest("  ", null));
        Assert.Equal(HttpStatusCode.BadRequest, response.StatusCode);
    }

    [Fact]
    public async Task CreateReturnsTheNewSubject()
    {
        var response = await _client.PostAsJsonAsync("/api/subjects", new CreateSubjectRequest("  Giulia  ", " Centro "));
        Assert.Equal(HttpStatusCode.Created, response.StatusCode);
        var item = await response.Content.ReadFromJsonAsync<Subject>();
        Assert.Equal("Giulia", item!.Name);
        Assert.Equal("Centro", item.Zone);
    }

    [Fact]
    public async Task UpdateReturnsNotFoundForUnknownId()
    {
        var response = await _client.PutAsJsonAsync("/api/subjects/999", new CreateSubjectRequest("Giulia", null));
        Assert.Equal(HttpStatusCode.NotFound, response.StatusCode);
    }

    [Fact]
    public async Task UpdateReturnsTheChangedSubject()
    {
        var response = await _client.PutAsJsonAsync("/api/subjects/1", new CreateSubjectRequest("Giulia", "Ovest"));
        Assert.Equal(HttpStatusCode.OK, response.StatusCode);
        var item = await response.Content.ReadFromJsonAsync<Subject>();
        Assert.Equal("Giulia", item!.Name);
        Assert.Equal("Ovest", item.Zone);
    }

    [Fact]
    public async Task DeleteReturnsNoContentForAnExistingSubject()
    {
        var response = await _client.DeleteAsync("/api/subjects/3");
        Assert.Equal(HttpStatusCode.NoContent, response.StatusCode);
    }

    [Fact]
    public async Task DeleteReturnsNotFoundForAnUnknownId()
    {
        var response = await _client.DeleteAsync("/api/subjects/999");
        Assert.Equal(HttpStatusCode.NotFound, response.StatusCode);
    }
}
'''

    test_project = f'''<Project Sdk="Microsoft.NET.Sdk">
  <PropertyGroup>
    <TargetFramework>net10.0</TargetFramework>
    <ImplicitUsings>enable</ImplicitUsings>
    <Nullable>enable</Nullable>
    <IsPackable>false</IsPackable>
    <IsTestProject>true</IsTestProject>
  </PropertyGroup>
  <ItemGroup>
    <PackageReference Include="Microsoft.NET.Test.Sdk" Version="{TEST_SDK_VERSION}" />
    <PackageReference Include="xunit" Version="{XUNIT_VERSION}" />
    <PackageReference Include="xunit.runner.visualstudio" Version="{XUNIT_RUNNER_VERSION}" />
{_integration_test_reference(lab)}{_ef_test_reference(lab)}
  </ItemGroup>
  <ItemGroup>
    <ProjectReference Include="../Server.csproj" />
  </ItemGroup>
</Project>
'''
    source_files["Server.csproj"] = server_csproj
    source_files["Tests/Server.Tests.csproj"] = test_project
    source_files["Tests/LabTests.cs"] = "using Xunit;\n\n" + test_source
    if ef_lab:
        source_files[".config/dotnet-tools.json"] = json.dumps({
            "version": 1, "isRoot": True,
            "tools": {"dotnet-ef": {"version": "10.0.12", "commands": ["dotnet-ef"]}},
        }, indent=2)
    _write_missing(server, source_files)


def _integration_test_reference(lab: Lab) -> str:
    api_lab_ids = {"lab-aspnet-minimal-api", "lab-fullstack-jwt-auth", "lab-fullstack-monorepo-crud", "lab-portfolio-enterprise"}
    if lab.id in api_lab_ids:
        return '    <PackageReference Include="Microsoft.AspNetCore.Mvc.Testing" Version="10.0.12" />\n'
    return ""


def _ef_test_reference(lab: Lab) -> str:
    if lab.id == "lab-efcore-sqlite-db":
        return '    <PackageReference Include="Microsoft.EntityFrameworkCore.Sqlite" Version="10.0.12" />\n'
    return ""


def _subjects_api_files(lab: Lab) -> dict[str, str]:
    return {
        "Program.cs": '''using Dev48Lab;

var builder = WebApplication.CreateBuilder(args);
builder.Services.AddCors(options => options.AddDefaultPolicy(policy =>
    policy.WithOrigins("http://localhost:4200").AllowAnyHeader().AllowAnyMethod()));
builder.Services.AddSingleton<SubjectStore>();
var app = builder.Build();
app.UseCors();

app.MapGet("/api/subjects", (SubjectStore store) => Results.Ok(store.GetAll()));
app.MapPost("/api/subjects", (CreateSubjectRequest request, SubjectStore store) =>
{
    if (string.IsNullOrWhiteSpace(request.Name)) return Results.BadRequest(new { error = "Name is required." });
    var created = store.Add(request);
    return Results.Created($"/api/subjects/{created.Id}", created);
});
app.MapPut("/api/subjects/{id:int}", (int id, CreateSubjectRequest request, SubjectStore store) =>
{
    if (string.IsNullOrWhiteSpace(request.Name)) return Results.BadRequest(new { error = "Name is required." });
    var updated = store.Update(id, request);
    return updated is null ? Results.NotFound() : Results.Ok(updated);
});
app.MapDelete("/api/subjects/{id:int}", (int id, SubjectStore store) =>
    store.Remove(id) ? Results.NoContent() : Results.NotFound());
app.Run();

public partial class Program { }
''',
        "SubjectStore.cs": '''namespace Dev48Lab;

public record Subject(int Id, string Name, string Zone, bool Active);
public record CreateSubjectRequest(string Name, string? Zone);

public sealed class SubjectStore
{
    private readonly List<Subject> _subjects = [
        new(1, "Mario Rossi", "Centro", true),
        new(2, "Anna Bianchi", "Nord", false),
        new(3, "Paolo Verdi", "Sud", true)
    ];

    public IReadOnlyList<Subject> GetAll() => _subjects.ToArray();

    public Subject Add(CreateSubjectRequest request) => throw new NotImplementedException("Completa la creazione del soggetto.");

    public Subject? Update(int id, CreateSubjectRequest request) => throw new NotImplementedException("Completa l'aggiornamento del soggetto.");

    public bool Remove(int id)
    {
        var subject = _subjects.FirstOrDefault(item => item.Id == id);
        if (subject is null) return false;
        _subjects.Remove(subject);
        return true;
    }
}
'''
    }


def _jwt_api_files() -> dict[str, str]:
    return {
        "Program.cs": '''using System.IdentityModel.Tokens.Jwt;
using System.Security.Claims;
using System.Text;
using Dev48Lab;
using Microsoft.AspNetCore.Authentication.JwtBearer;
using Microsoft.IdentityModel.Tokens;

var builder = WebApplication.CreateBuilder(args);
builder.Services.AddCors(options => options.AddPolicy("AngularClient", policy =>
    policy.WithOrigins("http://localhost:4200").AllowAnyHeader().AllowAnyMethod()));
var signingKey = builder.Configuration["Jwt:SigningKey"]
    ?? throw new InvalidOperationException("Configura Jwt:SigningKey fuori dal repository.");
var key = new SymmetricSecurityKey(Encoding.UTF8.GetBytes(signingKey));
builder.Services.AddAuthentication(JwtBearerDefaults.AuthenticationScheme).AddJwtBearer(options =>
{
    options.TokenValidationParameters = new TokenValidationParameters
    {
        ValidateIssuer = true, ValidIssuer = "dev48-lab",
        ValidateAudience = true, ValidAudience = "dev48-client",
        ValidateIssuerSigningKey = true, IssuerSigningKey = key,
        ValidateLifetime = true, ClockSkew = TimeSpan.FromSeconds(30)
    };
});
builder.Services.AddAuthorization(options =>
    options.AddPolicy("AdminOnly", policy => policy.RequireRole("Admin")));
var app = builder.Build();
app.UseCors("AngularClient");
app.UseAuthentication();
app.UseAuthorization();

app.MapPost("/api/login", (LoginRequest request) =>
{
    string? role = request.UserName switch
    {
        "demo" => "Reader",
        "admin" => "Admin",
        _ => null
    };
    if (request.Password != "demo" || role is null) return Results.Unauthorized();
    // TODO: crea e firma un token breve con claim di nome e ruolo, issuer, audience e scadenza.
    return Results.StatusCode(StatusCodes.Status501NotImplemented);
});
app.MapGet("/api/profile", (ClaimsPrincipal user) => Results.Ok(new { name = user.Identity?.Name }))
    .RequireAuthorization();
app.MapGet("/api/admin", () => Results.Ok("Area amministrativa"))
    .RequireAuthorization("AdminOnly");
app.Run();

public partial class Program { }
''',
        "AuthContracts.cs": '''namespace Dev48Lab;

public record LoginRequest(string UserName, string Password);
public record LoginResponse(string Token);
'''
    }


def _ensure_angular_project(client: Path, lab: Lab) -> None:
    project_name = f"{lab.id.replace('-', '')}client"
    package = {
        "name": project_name,
        "version": "1.0.0",
        "private": True,
        "scripts": {"start": "ng serve", "build": "ng build", "test": "ng test --watch=false && ng build"},
        "dependencies": {
            "@angular/common": f"^{ANGULAR_VERSION}",
            "@angular/compiler": f"^{ANGULAR_VERSION}",
            "@angular/core": f"^{ANGULAR_VERSION}",
            "@angular/forms": f"^{ANGULAR_VERSION}",
            "@angular/platform-browser": f"^{ANGULAR_VERSION}",
            "@angular/router": f"^{ANGULAR_VERSION}",
            "rxjs": "~7.8.0",
            "tslib": "^2.3.0"
        },
        "devDependencies": {
            "@angular/build": f"^{ANGULAR_VERSION}",
            "@angular/cli": f"^{ANGULAR_VERSION}",
            "@angular/compiler-cli": f"^{ANGULAR_VERSION}",
            "jsdom": "^30.0.0",
            "typescript": "~6.0.2",
            "vitest": "^5.0.0"
        }
    }
    app_ts, app_html, app_spec, extras = _angular_lab_sources(lab)
    routes = extras.pop("src/app/app.routes.ts", "import { Routes } from '@angular/router';\n\nexport const routes: Routes = [];\n")
    app_config = extras.pop(
        "src/app/app.config.ts",
        "import { ApplicationConfig, provideBrowserGlobalErrorListeners } from '@angular/core';\n"
        "import { provideRouter } from '@angular/router';\nimport { routes } from './app.routes';\n\n"
        "export const appConfig: ApplicationConfig = { providers: [provideBrowserGlobalErrorListeners(), provideRouter(routes)] };\n",
    )
    files = {
        "package.json": json.dumps(package, ensure_ascii=False, indent=2),
        "angular.json": json.dumps(_angular_json(project_name), indent=2),
        "tsconfig.json": json.dumps(_tsconfig(), indent=2),
        "tsconfig.app.json": json.dumps({"extends": "./tsconfig.json", "compilerOptions": {"types": []}, "include": ["src/**/*.ts"], "exclude": ["src/**/*.spec.ts"]}, indent=2),
        "tsconfig.spec.json": json.dumps({"extends": "./tsconfig.json", "compilerOptions": {"types": ["vitest/globals"]}, "include": ["src/**/*.d.ts", "src/**/*.spec.ts"]}, indent=2),
        "src/index.html": f'<!doctype html><html lang="it"><head><meta charset="utf-8"><title>{escape(lab.title)}</title><base href="/"><meta name="viewport" content="width=device-width, initial-scale=1"></head><body><app-root></app-root></body></html>',
        "src/main.ts": "import { bootstrapApplication } from '@angular/platform-browser';\nimport { appConfig } from './app/app.config';\nimport { App } from './app/app';\n\nbootstrapApplication(App, appConfig).catch(error => console.error(error));\n",
        "src/styles.css": "body { margin: 0; font-family: system-ui, sans-serif; color: #172033; }\nmain { max-width: 56rem; margin: 2rem auto; padding: 1rem; }\nbutton, input { font: inherit; }\n:focus-visible { outline: 3px solid #2563eb; outline-offset: 2px; }\n",
        "src/app/app.ts": app_ts,
        "src/app/app.html": app_html,
        "src/app/app.css": "",
        "src/app/app.routes.ts": routes,
        "src/app/app.config.ts": app_config,
        "src/app/app.spec.ts": app_spec,
    }
    files.update(extras)
    _write_missing(client, files)


def _angular_json(project_name: str) -> dict:
    return {
        "$schema": "./node_modules/@angular/cli/lib/config/schema.json",
        "version": 1,
        "cli": {"packageManager": "npm"},
        "projects": {project_name: {
            "projectType": "application", "root": "", "sourceRoot": "src", "prefix": "app",
            "architect": {
                "build": {
                    "builder": "@angular/build:application",
                    "options": {"browser": "src/main.ts", "tsConfig": "tsconfig.app.json", "assets": [], "styles": ["src/styles.css"]},
                    "configurations": {"production": {"outputHashing": "all"}, "development": {"optimization": False, "extractLicenses": False, "sourceMap": True}},
                    "defaultConfiguration": "production"
                },
                "serve": {"builder": "@angular/build:dev-server", "configurations": {"production": {"buildTarget": f"{project_name}:build:production"}, "development": {"buildTarget": f"{project_name}:build:development"}}, "defaultConfiguration": "development"},
                "test": {"builder": "@angular/build:unit-test"}
            }
        }}
    }


def _tsconfig() -> dict:
    return {
        "compileOnSave": False,
        "compilerOptions": {
            "noImplicitOverride": True, "noPropertyAccessFromIndexSignature": True,
            "noImplicitReturns": True, "noFallthroughCasesInSwitch": True,
            "skipLibCheck": True, "isolatedModules": True, "experimentalDecorators": True,
            "importHelpers": True, "target": "ES2022", "module": "preserve",
            "strict": True
        },
        "angularCompilerOptions": {"strictInjectionParameters": True, "strictInputAccessModifiers": True, "strictTemplates": True},
        "files": [], "references": [{"path": "./tsconfig.app.json"}, {"path": "./tsconfig.spec.json"}]
    }


def _angular_lab_sources(lab: Lab) -> tuple[str, str, str, dict[str, str]]:
    title = json.dumps(lab.title, ensure_ascii=False)
    summary = json.dumps(lab.description, ensure_ascii=False)
    tasks = json.dumps(list(lab.requirements), ensure_ascii=False)
    component = '''import { Component, computed, signal } from '@angular/core';

interface LabTask { id: number; text: string; done: boolean; }

@Component({
  selector: 'app-root',
  templateUrl: './app.html',
  styleUrl: './app.css'
})
export class App {
  readonly title = TITLE;
  readonly description = DESCRIPTION;
  readonly tasks = signal<string[]>(REQUIREMENTS);
  readonly completed = signal<number[]>([]);
  readonly completedCount = computed(() => this.completed().length);

  isDone(index: number): boolean { return this.completed().includes(index); }
  toggle(index: number): void {
    this.completed.update(current => current.includes(index)
      ? current.filter(item => item !== index)
      : [...current, index]);
  }
}
'''.replace("TITLE", title).replace("DESCRIPTION", summary).replace("REQUIREMENTS", tasks)
    template = '''<main>
  <p class="eyebrow">DEV//48 · LAB</p>
  <h1>{{ title }}</h1>
  <p>{{ description }}</p>
  <p aria-live="polite">{{ completedCount() }} / {{ tasks().length }} requisiti segnati</p>
  @if (tasks().length > 0) {
    <ul>
      @for (task of tasks(); track $index) {
        <li>
          <span [class.done]="isDone($index)">{{ task }}</span>
          <button type="button" (click)="toggle($index)">
            {{ isDone($index) ? 'Annulla' : 'Segna come fatto' }}
          </button>
        </li>
      }
    </ul>
  } @else {
    <p role="status">Aggiungi il primo requisito per iniziare.</p>
  }
</main>
'''
    spec = '''import { TestBed } from '@angular/core/testing';
import { App } from './app';

describe('Lab requirements checklist', () => {
  beforeEach(async () => {
    await TestBed.configureTestingModule({ imports: [App] }).compileComponents();
  });

  it('shows the lab title and requirements', () => {
    const fixture = TestBed.createComponent(App);
    fixture.detectChanges();
    const element = fixture.nativeElement as HTMLElement;
    expect(element.querySelector('h1')?.textContent).toContain(TITLE_TEXT);
    expect(element.querySelectorAll('li').length).toBe(REQUIREMENT_COUNT);
  });

  it('updates the visible completion count after a click', () => {
    const fixture = TestBed.createComponent(App);
    fixture.detectChanges();
    const button = fixture.nativeElement.querySelector('button') as HTMLButtonElement;
    button.click();
    fixture.detectChanges();
    expect(fixture.nativeElement.querySelector('[aria-live]')?.textContent).toContain('1 /');
  });
});
'''.replace("TITLE_TEXT", title).replace("REQUIREMENT_COUNT", str(len(lab.requirements)))
    extras = {"src/app/app.routes.ts": "import { Routes } from '@angular/router';\n\nexport const routes: Routes = [];\n"}
    if lab.id == "lab-angular-standalone":
        component = '''import { Component, computed, signal } from '@angular/core';

interface Product { id: number; name: string; description: string; }
const initialProducts: Product[] = [
  { id: 1, name: 'Taccuino A5', description: 'Carta a righe, copertina blu.' },
  { id: 2, name: 'Penna nera', description: 'Punta fine per appunti.' },
  { id: 3, name: 'Zaino', description: 'Zaino leggero da lavoro.' },
];

@Component({ selector: 'app-root', templateUrl: './app.html', styleUrl: './app.css' })
export class App {
  readonly title = TITLE;
  readonly description = DESCRIPTION;
  readonly products = signal(initialProducts);
  readonly query = signal('');
  readonly selected = signal<Product | null>(null);
  readonly visibleProducts = computed(() => this.products()); // TODO: filtra usando query().

  updateQuery(event: Event): void {
    this.query.set((event.target as HTMLInputElement).value);
  }
  select(product: Product): void { this.selected.set(product); }
}
'''.replace("TITLE", title).replace("DESCRIPTION", summary)
        template = '''<main>
  <h1>{{ title }}</h1>
  <p>{{ description }}</p>
  <label for="catalog-search">Cerca un prodotto</label>
  <input id="catalog-search" type="search" (input)="updateQuery($event)">
  <ul aria-label="Catalogo prodotti">
    @for (product of visibleProducts(); track product.id) {
      <li><button type="button" (click)="select(product)">Apri {{ product.name }}</button></li>
    } @empty {
      <li role="status">Nessun prodotto trovato.</li>
    }
  </ul>
  @if (selected(); as product) {
    <section aria-label="Dettaglio prodotto"><h2>{{ product.name }}</h2><p>{{ product.description }}</p></section>
  }
</main>
'''
        spec = '''import { TestBed } from '@angular/core/testing';
import { App } from './app';

describe('Catalog component', () => {
  beforeEach(async () => { await TestBed.configureTestingModule({ imports: [App] }).compileComponents(); });

  it('renders the three catalog items', () => {
    const fixture = TestBed.createComponent(App);
    fixture.detectChanges();
    expect(fixture.nativeElement.querySelectorAll('li').length).toBe(3);
  });

  it('filters the list and shows a useful empty state', () => {
    const fixture = TestBed.createComponent(App);
    fixture.detectChanges();
    const input = fixture.nativeElement.querySelector('#catalog-search') as HTMLInputElement;
    input.value = 'taccuino';
    input.dispatchEvent(new Event('input'));
    fixture.detectChanges();
    expect(fixture.nativeElement.querySelectorAll('li').length).toBe(1);
    input.value = 'inesistente';
    input.dispatchEvent(new Event('input'));
    fixture.detectChanges();
    expect(fixture.nativeElement.querySelector('[role="status"]')?.textContent).toContain('Nessun prodotto');
  });

  it('shows details after selecting a product', () => {
    const fixture = TestBed.createComponent(App);
    fixture.detectChanges();
    (fixture.nativeElement.querySelector('button') as HTMLButtonElement).click();
    fixture.detectChanges();
    expect(fixture.nativeElement.querySelector('[aria-label="Dettaglio prodotto"] h2')?.textContent).toContain('Taccuino A5');
  });
});
'''
    if lab.id == "lab-angular-signals-state":
        component = '''import { Component, computed, signal } from '@angular/core';

interface Metric { id: number; name: string; value: number; }

@Component({ selector: 'app-root', templateUrl: './app.html', styleUrl: './app.css' })
export class App {
  readonly title = TITLE;
  readonly description = DESCRIPTION;
  readonly goal = 50;
  readonly metrics = signal<Metric[]>([
    { id: 1, name: 'Utenti', value: 24 },
    { id: 2, name: 'Ordini', value: 18 },
  ]);
  readonly total = computed(() => this.metrics().length); // TODO: somma i valori, non il numero di righe.
  readonly percentage = computed(() => Math.round(this.total() / this.goal * 100));

  removeMetric(id: number): void { this.metrics.update(items => items.filter(item => item.id !== id)); }
  addMetric(): void {
    this.metrics.update(items => [...items, { id: Math.max(0, ...items.map(item => item.id)) + 1, name: 'Nuova metrica', value: 5 }]);
  }
}
'''.replace("TITLE", title).replace("DESCRIPTION", summary)
        template = '''<main>
  <h1>{{ title }}</h1><p>{{ description }}</p>
  <p>Totale: <output data-testid="total">{{ total() }}</output></p>
  <p>Obiettivo raggiunto: <output data-testid="percentage">{{ percentage() }}%</output></p>
  @if (metrics().length === 0) { <p role="status">Nessuna metrica.</p> }
  <ul>
    @for (metric of metrics(); track metric.id) {
      <li>{{ metric.name }}: {{ metric.value }} <button type="button" (click)="removeMetric(metric.id)">Rimuovi {{ metric.name }}</button></li>
    }
  </ul>
  <button type="button" (click)="addMetric()">Aggiungi metrica</button>
</main>
'''
        spec = '''import { TestBed } from '@angular/core/testing';
import { App } from './app';

describe('Signals metrics dashboard', () => {
  beforeEach(async () => { await TestBed.configureTestingModule({ imports: [App] }).compileComponents(); });

  it('derives a total and percentage from metric values', () => {
    const fixture = TestBed.createComponent(App);
    fixture.detectChanges();
    expect(fixture.nativeElement.querySelector('[data-testid="total"]')?.textContent.trim()).toBe('42');
    expect(fixture.nativeElement.querySelector('[data-testid="percentage"]')?.textContent.trim()).toBe('84%');
  });

  it('updates the derived total after removing and adding a metric', () => {
    const fixture = TestBed.createComponent(App);
    fixture.detectChanges();
    (fixture.nativeElement.querySelector('button') as HTMLButtonElement).click();
    fixture.detectChanges();
    expect(fixture.nativeElement.querySelector('[data-testid="total"]')?.textContent.trim()).toBe('18');
    const addButton = Array.from(fixture.nativeElement.querySelectorAll('button') as NodeListOf<HTMLButtonElement>)
      .find(button => button.textContent?.includes('Aggiungi metrica'));
    expect(addButton).toBeDefined();
    addButton!.click();
    fixture.detectChanges();
    expect(fixture.nativeElement.querySelector('[data-testid="total"]')?.textContent.trim()).toBe('23');
  });
});
'''
    if lab.id == "lab-testing-xunit-vitest":
        component = '''import { Component, signal } from '@angular/core';

interface Subject { id: number; name: string; }

@Component({ selector: 'app-root', templateUrl: './app.html', styleUrl: './app.css' })
export class App {
  readonly title = TITLE;
  readonly subjects = signal<Subject[]>([{ id: 1, name: 'Mario' }, { id: 2, name: 'Anna' }]);
  remove(id: number): void { this.subjects.update(items => items.filter(item => item.id !== id)); }
}
'''.replace("TITLE", title)
        template = '''<main>
  <h1>{{ title }}</h1>
  <p>Usa i test per descrivere i comportamenti che il componente deve mantenere.</p>
  <ul>@for (subject of subjects(); track subject.id) {
    <li>{{ subject.name }} <button type="button" (click)="remove(subject.id)">Elimina {{ subject.name }}</button></li>
  }</ul>
</main>
'''
        spec = '''import { TestBed } from '@angular/core/testing';
import { App } from './app';

describe('Subjects list component', () => {
  beforeEach(async () => { await TestBed.configureTestingModule({ imports: [App] }).compileComponents(); });

  it('renders the initial subjects', () => {
    const fixture = TestBed.createComponent(App);
    fixture.detectChanges();
    expect(fixture.nativeElement.querySelectorAll('li').length).toBe(2);
    expect(fixture.nativeElement.textContent).toContain('Mario');
  });

  it('removes only the selected subject', () => {
    const fixture = TestBed.createComponent(App);
    fixture.detectChanges();
    (fixture.nativeElement.querySelector('button') as HTMLButtonElement).click();
    fixture.detectChanges();
    expect(fixture.nativeElement.textContent).not.toContain('Mario');
    expect(fixture.nativeElement.textContent).toContain('Anna');
  });
});
'''
    if lab.id == "lab-ts-angular-models":
        component = '''import { Component } from '@angular/core';
import { describeOrder, OrderState } from './order';

@Component({ selector: 'app-root', templateUrl: './app.html', styleUrl: './app.css' })
export class App {
  readonly title = TITLE;
  readonly description = DESCRIPTION;
  readonly example: OrderState = { status: 'ready', order: { id: 42, total: 20 } };
  readonly summary = describeOrder(this.example);
}
'''.replace("TITLE", title).replace("DESCRIPTION", summary)
        template = '<main><h1>{{ title }}</h1><p>{{ description }}</p><p>Stato esempio: {{ summary }}</p></main>'
        spec = '''import { TestBed } from '@angular/core/testing';
import { App } from './app';
describe('Typed order example', () => {
  it('renders the summary derived from a typed state', async () => {
    await TestBed.configureTestingModule({ imports: [App] }).compileComponents();
    const fixture = TestBed.createComponent(App);
    fixture.detectChanges();
    expect(fixture.nativeElement.textContent).toContain('Ordine #42');
  });
});
'''
        extras["src/app/order.ts"] = '''export interface OrderDto { id: number; total: number; }
export type OrderState =
  | { status: 'loading' }
  | { status: 'ready'; order: OrderDto }
  | { status: 'error'; message: string }
  | { status: 'cancelled'; reason: string };
export function describeOrder(state: OrderState): string {
  switch (state.status) {
    case 'loading': return 'Caricamento';
    case 'ready': return `Ordine #${state.order.id}`;
    case 'error': return state.message;
    case 'cancelled': return ''; // TODO: mostra il motivo dell'annullamento.
  }
}
'''
        extras["src/app/order.spec.ts"] = '''import { describeOrder } from './order';

describe('OrderState', () => {
  it('describes each variant without reading fields from another state', () => {
    expect(describeOrder({ status: 'loading' })).toBe('Caricamento');
    expect(describeOrder({ status: 'ready', order: { id: 42, total: 20 } })).toBe('Ordine #42');
    expect(describeOrder({ status: 'error', message: 'Rete non disponibile' })).toBe('Rete non disponibile');
    expect(describeOrder({ status: 'cancelled', reason: 'Richiesto dal cliente' })).toBe('Annullato: Richiesto dal cliente');
  });
});
'''
    if lab.id == "lab-fullstack-jwt-auth":
        component = '''import { Component } from '@angular/core';
@Component({ selector: 'app-root', templateUrl: './app.html', styleUrl: './app.css' })
export class App { readonly title = TITLE; readonly description = DESCRIPTION; }
'''.replace("TITLE", title).replace("DESCRIPTION", summary)
        template = '<main><h1>{{ title }}</h1><p>{{ description }}</p><p>Il token deve essere inviato solo all’origine dell’API configurata.</p></main>'
        spec = '''import { TestBed } from '@angular/core/testing';
import { App } from './app';

describe('JWT lab page', () => {
  it('explains the token destination rule', async () => {
    await TestBed.configureTestingModule({ imports: [App] }).compileComponents();
    const fixture = TestBed.createComponent(App);
    fixture.detectChanges();
    expect(fixture.nativeElement.querySelector('h1')?.textContent).toContain('Autenticazione JWT');
    expect(fixture.nativeElement.textContent).toContain('solo all’origine dell’API configurata');
  });
});
'''
        extras["src/app/session.service.ts"] = '''import { Injectable, signal } from '@angular/core';

@Injectable({ providedIn: 'root' })
export class SessionService {
  readonly token = signal<string | null>(null);
}
'''
        extras["src/app/auth.interceptor.ts"] = '''import { inject } from '@angular/core';
import { DOCUMENT } from '@angular/common';
import { HttpInterceptorFn } from '@angular/common/http';
import { SessionService } from './session.service';

export const API_ORIGIN = 'http://localhost:5000';

export const authInterceptor: HttpInterceptorFn = (request, next) => {
  const token = inject(SessionService).token();
  const isApiRequest = new URL(request.url, inject(DOCUMENT).baseURI).origin === API_ORIGIN;
  if (!token || !isApiRequest) return next(request);
  // TODO: clona la richiesta impostando Authorization: Bearer <token>.
  return next(request);
};
'''
        extras["src/app/auth.interceptor.spec.ts"] = '''import { TestBed } from '@angular/core/testing';
import { DOCUMENT } from '@angular/common';
import { HttpClient, provideHttpClient, withInterceptors } from '@angular/common/http';
import { provideHttpClientTesting, HttpTestingController } from '@angular/common/http/testing';
import { authInterceptor, API_ORIGIN } from './auth.interceptor';
import { SessionService } from './session.service';

describe('JWT HTTP interceptor', () => {
  beforeEach(() => TestBed.configureTestingModule({ providers: [
    provideHttpClient(withInterceptors([authInterceptor])), provideHttpClientTesting(),
    { provide: DOCUMENT, useValue: { baseURI: 'http://localhost:4200/' } }
  ] }));
  afterEach(() => TestBed.inject(HttpTestingController).verify());

  it('adds the Bearer token to the configured API origin', () => {
    TestBed.inject(SessionService).token.set('demo-token');
    TestBed.inject(HttpClient).get(`${API_ORIGIN}/api/profile`).subscribe();
    const request = TestBed.inject(HttpTestingController).expectOne(`${API_ORIGIN}/api/profile`);
    expect(request.request.headers.get('Authorization')).toBe('Bearer demo-token');
    request.flush({ name: 'demo' });
  });

  it('never sends the token to another origin', () => {
    TestBed.inject(SessionService).token.set('demo-token');
    TestBed.inject(HttpClient).get('https://example.test/profile').subscribe();
    const request = TestBed.inject(HttpTestingController).expectOne('https://example.test/profile');
    expect(request.request.headers.has('Authorization')).toBe(false);
    request.flush({});
  });
  it('resolves relative URLs against the page, not the API origin', () => {
    TestBed.inject(SessionService).token.set('demo-token');
    TestBed.inject(HttpClient).get('/api/profile').subscribe();
    const request = TestBed.inject(HttpTestingController).expectOne('/api/profile');
    expect(request.request.headers.has('Authorization')).toBe(false);
    request.flush({});
  });
  it('keeps the request unchanged when no token is available', () => {
    TestBed.inject(HttpClient).get(`${API_ORIGIN}/api/profile`).subscribe();
    const request = TestBed.inject(HttpTestingController).expectOne(`${API_ORIGIN}/api/profile`);
    expect(request.request.headers.has('Authorization')).toBe(false);
    request.flush({});
  });
});
'''
        extras["src/app/app.config.ts"] = "import { ApplicationConfig, provideBrowserGlobalErrorListeners } from '@angular/core';\nimport { provideHttpClient, withInterceptors } from '@angular/common/http';\nimport { provideRouter } from '@angular/router';\nimport { authInterceptor } from './auth.interceptor';\nimport { routes } from './app.routes';\n\nexport const appConfig: ApplicationConfig = { providers: [provideBrowserGlobalErrorListeners(), provideRouter(routes), provideHttpClient(withInterceptors([authInterceptor]))] };\n"
    if lab.id in {"lab-fullstack-monorepo-crud", "lab-portfolio-enterprise"}:
        component = '''import { Component, OnInit, inject, signal } from '@angular/core';
import { Subject, SubjectsService } from './subjects.service';

@Component({ selector: 'app-root', templateUrl: './app.html', styleUrl: './app.css' })
export class App implements OnInit {
  readonly title = TITLE;
  readonly description = DESCRIPTION;
  readonly subjects = signal<Subject[]>([]);
  readonly loading = signal(false);
  readonly error = signal<string | null>(null);
  private readonly service = inject(SubjectsService);

  ngOnInit(): void {
    this.loading.set(true);
    this.service.list().subscribe({
      next: items => { this.subjects.set(items); this.loading.set(false); },
      error: () => { this.error.set('Non è stato possibile caricare i dati.'); this.loading.set(false); }
    });
  }
}
'''.replace("TITLE", title).replace("DESCRIPTION", summary)
        template = '''<main>
  <h1>{{ title }}</h1><p>{{ description }}</p>
  @if (loading()) { <p role="status">Caricamento…</p> }
  @if (error(); as message) { <p role="alert">{{ message }}</p> }
  @if (!loading() && !error() && subjects().length === 0) { <p role="status">Nessun soggetto presente.</p> }
  <ul>@for (subject of subjects(); track subject.id) { <li>{{ subject.name }} · {{ subject.zone }}</li> }</ul>
</main>
'''
        spec = '''import { TestBed } from '@angular/core/testing';
import { provideHttpClient } from '@angular/common/http';
import { provideHttpClientTesting, HttpTestingController } from '@angular/common/http/testing';
import { App } from './app';
import { API_ORIGIN } from './subjects.service';

describe('Subjects page', () => {
  beforeEach(async () => {
    await TestBed.configureTestingModule({ imports: [App], providers: [provideHttpClient(), provideHttpClientTesting()] }).compileComponents();
  });
  it('shows subjects received from the API', () => {
    const fixture = TestBed.createComponent(App);
    fixture.detectChanges();
    const http = TestBed.inject(HttpTestingController);
    http.expectOne(`${API_ORIGIN}/api/subjects`).flush([{ id: 1, name: 'Mario', zone: 'Centro', active: true }]);
    fixture.detectChanges();
    expect(fixture.nativeElement.textContent).toContain('Mario');
    http.verify();
  });
});
'''
        extras["src/app/subjects.service.ts"] = '''import { inject, Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, of } from 'rxjs';

export interface Subject { id: number; name: string; zone: string; active: boolean; }
export interface SubjectInput { name: string; zone: string; }
export const API_ORIGIN = 'http://localhost:5000';

@Injectable({ providedIn: 'root' })
export class SubjectsService {
  private readonly http = inject(HttpClient);
  private readonly endpoint = `${API_ORIGIN}/api/subjects`;

  list(): Observable<Subject[]> {
    // TODO: effettua GET sull'endpoint tipizzato.
    return of([]);
  }
  create(input: SubjectInput): Observable<Subject> { return this.http.post<Subject>(this.endpoint, input); }
  update(id: number, input: SubjectInput): Observable<Subject> { return this.http.put<Subject>(`${this.endpoint}/${id}`, input); }
  remove(id: number): Observable<void> { return this.http.delete<void>(`${this.endpoint}/${id}`); }
}
'''
        extras["src/app/subjects.service.spec.ts"] = '''import { TestBed } from '@angular/core/testing';
import { provideHttpClient } from '@angular/common/http';
import { provideHttpClientTesting, HttpTestingController } from '@angular/common/http/testing';
import { SubjectsService, API_ORIGIN } from './subjects.service';

describe('SubjectsService', () => {
  beforeEach(() => TestBed.configureTestingModule({ providers: [provideHttpClient(), provideHttpClientTesting()] }));
  afterEach(() => TestBed.inject(HttpTestingController).verify());

  it('loads the typed collection from the API', () => {
    const result: unknown[] = [];
    TestBed.inject(SubjectsService).list().subscribe(items => result.push(...items));
    const request = TestBed.inject(HttpTestingController).expectOne(`${API_ORIGIN}/api/subjects`);
    expect(request.request.method).toBe('GET');
    request.flush([{ id: 1, name: 'Mario', zone: 'Centro', active: true }]);
    expect(result).toHaveLength(1);
  });
});
'''
        extras["src/app/app.config.ts"] = "import { ApplicationConfig, provideBrowserGlobalErrorListeners } from '@angular/core';\nimport { provideHttpClient } from '@angular/common/http';\nimport { provideRouter } from '@angular/router';\nimport { routes } from './app.routes';\n\nexport const appConfig: ApplicationConfig = { providers: [provideBrowserGlobalErrorListeners(), provideRouter(routes), provideHttpClient()] };\n"
    if lab.id == "lab-angular-reactive-forms":
        component = '''import { Component, inject } from '@angular/core';
import { AsyncValidatorFn, FormBuilder, ReactiveFormsModule, Validators } from '@angular/forms';
import { map, timer } from 'rxjs';

@Component({ selector: 'app-root', imports: [ReactiveFormsModule], templateUrl: './app.html', styleUrl: './app.css' })
export class App {
  private readonly fb = inject(FormBuilder);
  readonly title = TITLE;
  readonly description = DESCRIPTION;
  private readonly emailAvailable: AsyncValidatorFn = control =>
    timer(5).pipe(map(() => {
      // TODO: segnala { emailTaken: true } quando l'indirizzo è già occupato.
      return null;
    }));
  readonly form = this.fb.group({ email: ['', {
    validators: [Validators.required, Validators.email],
    asyncValidators: [this.emailAvailable]
  }] });
  submitted = false;
  submit(): void { if (this.form.valid) this.submitted = true; }
}
'''.replace("TITLE", title).replace("DESCRIPTION", summary).replace("REQUIREMENTS", tasks)
        template = '''<main>
  <h1>{{ title }}</h1>
  <p>{{ description }}</p>
  <form [formGroup]="form" (ngSubmit)="submit()">
    <label for="email">Email</label>
    <input id="email" type="email" formControlName="email">
    @if (form.controls.email.invalid && form.controls.email.touched) {
      <p role="alert">Inserisci un indirizzo email valido.</p>
    }
    @if (form.pending) { <p role="status">Verifica disponibilità…</p> }
    @if (form.controls.email.hasError('emailTaken')) { <p role="alert">Indirizzo già utilizzato.</p> }
    @if (submitted) { <p role="status">Richiesta inviata.</p> }
    <button type="submit" [disabled]="form.invalid || form.pending">Invia</button>
  </form>
</main>
'''
        spec = '''import { AbstractControl } from '@angular/forms';
import { TestBed } from '@angular/core/testing';
import { App } from './app';

function waitForValidation(control: AbstractControl): Promise<void> {
  if (!control.pending) return Promise.resolve();
  return new Promise(resolve => {
    const subscription = control.statusChanges.subscribe(status => {
      if (status !== 'PENDING') {
        subscription.unsubscribe();
        resolve();
      }
    });
  });
}

describe('Reactive form lab', () => {
  beforeEach(async () => { await TestBed.configureTestingModule({ imports: [App] }).compileComponents(); });
  it('blocks an empty email and accepts a valid one', async () => {
    const fixture = TestBed.createComponent(App);
    fixture.detectChanges();
    const app = fixture.componentInstance;
    expect(app.form.invalid).toBe(true);
    app.form.controls.email.setValue('learner@example.test');
    expect(app.form.pending).toBe(true);
    fixture.detectChanges();
    expect(fixture.nativeElement.textContent).toContain('Verifica disponibilità');
    expect(fixture.nativeElement.querySelector('button').disabled).toBe(true);
    await waitForValidation(app.form.controls.email);
    fixture.detectChanges();
    expect(app.form.valid).toBe(true);
    app.submit();
    expect(app.submitted).toBe(true);
  });
  it('reports an email already in use and does not submit', async () => {
    const fixture = TestBed.createComponent(App);
    fixture.detectChanges();
    const app = fixture.componentInstance;
    app.form.controls.email.setValue('taken@example.test');
    expect(app.form.pending).toBe(true);
    await waitForValidation(app.form.controls.email);
    expect(app.form.controls.email.hasError('emailTaken')).toBe(true);
    fixture.detectChanges();
    expect(fixture.nativeElement.querySelector('[role="alert"]')?.textContent).toContain('già utilizzato');
    app.submit();
    expect(app.submitted).toBe(false);
  });
  it('shows a readable message for an invalid email', () => {
    const fixture = TestBed.createComponent(App);
    fixture.detectChanges();
    const control = fixture.componentInstance.form.controls.email;
    control.setValue('not-an-email');
    control.markAsTouched();
    fixture.detectChanges();
    expect(fixture.nativeElement.querySelector('[role="alert"]')?.textContent).toContain('email valido');
  });
});
'''
    if lab.id == "lab-angular-routing-guard":
        extras["src/app/auth.guard.ts"] = '''import { inject } from '@angular/core';
import { CanActivateFn, Router } from '@angular/router';
import { SessionService } from './session.service';

export const authGuard: CanActivateFn = route => {
  const session = inject(SessionService);
  const router = inject(Router);
  const requiredRole = route.data['role'] as string;
  // TODO: allow an authenticated matching role; otherwise return a login UrlTree.
  return router.parseUrl('/login');
};
'''
        extras["src/app/app.routes.ts"] = '''import { Routes } from '@angular/router';
import { authGuard } from './auth.guard';

export const routes: Routes = [
  { path: '', redirectTo: 'dashboard', pathMatch: 'full' },
  { path: 'login', loadComponent: () => import('./pages/login').then(module => module.LoginPage) },
  { path: 'dashboard', loadComponent: () => import('./pages/dashboard').then(module => module.DashboardPage) },
  { path: 'admin', data: { role: 'Admin' }, canActivate: [authGuard], loadComponent: () => import('./pages/admin').then(module => module.AdminPage) },
  { path: '**', redirectTo: 'dashboard' }
];
'''
        extras["src/app/session.service.ts"] = '''import { Injectable, signal } from '@angular/core';

@Injectable({ providedIn: 'root' })
export class SessionService {
  readonly authenticated = signal(false);
  readonly role = signal('Guest');
}
'''
        extras["src/app/pages/dashboard.ts"] = "import { Component } from '@angular/core';\n@Component({ standalone: true, template: '<h2>Dashboard pubblica</h2>' })\nexport class DashboardPage {}\n"
        extras["src/app/pages/admin.ts"] = "import { Component } from '@angular/core';\n@Component({ standalone: true, template: '<h2>Area amministrativa</h2>' })\nexport class AdminPage {}\n"
        extras["src/app/pages/login.ts"] = "import { Component } from '@angular/core';\n@Component({ standalone: true, template: '<h2>Accesso richiesto</h2>' })\nexport class LoginPage {}\n"
        component = '''import { Component } from '@angular/core';
import { RouterLink, RouterOutlet } from '@angular/router';

@Component({ selector: 'app-root', imports: [RouterLink, RouterOutlet], templateUrl: './app.html', styleUrl: './app.css' })
export class App { readonly title = TITLE; readonly description = DESCRIPTION; }
'''.replace("TITLE", title).replace("DESCRIPTION", summary)
        template = '''<main>
  <h1>{{ title }}</h1><p>{{ description }}</p>
  <nav aria-label="Navigazione"><a routerLink="/dashboard">Dashboard</a> · <a routerLink="/admin">Area amministrativa</a></nav>
  <router-outlet />
</main>
'''
        spec = '''import { TestBed } from '@angular/core/testing';
import { provideRouter } from '@angular/router';
import { App } from './app';
import { routes } from './app.routes';

describe('Routing app shell', () => {
  it('renders a router outlet and navigation links', async () => {
    await TestBed.configureTestingModule({ imports: [App], providers: [provideRouter(routes)] }).compileComponents();
    const fixture = TestBed.createComponent(App);
    fixture.detectChanges();
    expect(fixture.nativeElement.querySelector('router-outlet')).toBeTruthy();
    expect(fixture.nativeElement.querySelectorAll('a').length).toBe(2);
  });
});
'''
        extras["src/app/auth.guard.spec.ts"] = '''import { TestBed } from '@angular/core/testing';
import { ActivatedRouteSnapshot, provideRouter, Router, RouterStateSnapshot, UrlTree } from '@angular/router';
import { authGuard } from './auth.guard';
import { SessionService } from './session.service';
import { routes } from './app.routes';

describe('Functional route guard', () => {
  beforeEach(() => TestBed.configureTestingModule({ providers: [provideRouter(routes)] }));
  const checkGuard = () => {
    const route = { data: { role: 'Admin' } } as unknown as ActivatedRouteSnapshot;
    return TestBed.runInInjectionContext(() => authGuard(route, {} as RouterStateSnapshot));
  };

  it('redirects an anonymous user to login', () => {
    const result = checkGuard();
    expect(result).toBeInstanceOf(UrlTree);
    expect(TestBed.inject(Router).serializeUrl(result as UrlTree)).toBe('/login');
  });
  it('allows an authenticated user with the required role', () => {
    const session = TestBed.inject(SessionService);
    session.authenticated.set(true);
    session.role.set('Admin');
    expect(checkGuard()).toBe(true);
  });
  it('redirects an authenticated user with a different role', () => {
    const session = TestBed.inject(SessionService);
    session.authenticated.set(true);
    session.role.set('User');
    expect(checkGuard()).toBeInstanceOf(UrlTree);
  });
});
'''
    return component, template, spec, extras

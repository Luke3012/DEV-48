# Organizzazione Monorepo: client/ e server/

Mettere Angular e ASP.NET Core nello stesso repository facilita modifiche coordinate, ma i due programmi restano processi distinti. Il confine che li collega è HTTP: un tipo TypeScript non diventa automaticamente un tipo C# e i dati attraversano la rete come JSON.

### Nel percorso

Da conoscere: [Minimal API da zero: Program.cs e WebApplication](net-03-01-minimal-api-da-zero-programcs-e-web.md); [Progetto Angular Standalone e Bootstrap applicazione](net-04-01-progetto-angular-standalone-e-boots.md).

La lezione usa Users per rendere leggibile il percorso end-to-end; il laboratorio Gestionale Full-Stack Monorepo applica gli stessi passaggi al dominio Subjects. Implementa GET `/api/subjects` per la lista, poi POST, PUT e DELETE; collega la lettura prima dei comandi di modifica della UI. Le suite separate non dimostrano da sole la comunicazione tra i due processi: prova anche un'operazione dal browser.

## Il confine HTTP collega due applicazioni

### La stessa lista di utenti attraversa i due progetti
```text
UserListComponent (stato e template Angular)
  ↓
UserService (responsabilità API lato client)
  ↓ HttpClient GET /api/users
ASP.NET Core route handler
  ↓ DbContext / EF Core
SQLite: tabella Users
  ↑ righe → proiezione UserResponse[]
JSON HTTP 200
  ↑ Observable<UserDto[]> → stato del componente
template: lista, caricamento, vuoto o errore
```

Percorsi essenziali:
```text
client/src/app/users/user.service.ts
client/src/app/users/user-list.component.ts
server/Program.cs
server/Data/AppDbContext.cs
server/Services/UserService.cs
server/DTOs/UserResponse.cs
```

Il route handler delega il caso d'uso a un servizio applicativo. Il servizio legge dal database e proietta un DTO, così il client non riceve tutte le proprietà dell'entity:
```csharp
// Program.cs
builder.Services.AddScoped<UserService>(); // AppDbContext è già registrato con AddDbContext.
app.MapGet("/api/users", (UserService users, CancellationToken ct) =>
    users.ListAsync(ct));

// Services/UserService.cs
using Microsoft.EntityFrameworkCore;

public sealed class UserService(AppDbContext db)
{
    public Task<List<UserResponse>> ListAsync(CancellationToken ct) =>
        db.Users.AsNoTracking()
            .OrderBy(user => user.Name)
            .Select(user => new UserResponse(user.Id, user.Name))
            .ToListAsync(ct);
}

// DTOs/UserResponse.cs
public sealed record UserResponse(int Id, string Name);
```

Il service Angular richiede lo stesso percorso e dichiara il contratto che si aspetta:
```typescript
import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

export type UserDto = { id: number; name: string };

@Injectable({ providedIn: 'root' })
export class UserService {
  private readonly http = inject(HttpClient);
  list(): Observable<UserDto[]> { return this.http.get<UserDto[]>('/api/users'); }
}
```

Il componente si occupa della presentazione e del ciclo di caricamento. Questi estratti vivono in `user-list.component.ts`:
```typescript
import { Component, OnInit, inject, signal } from '@angular/core';
import { UserService, type UserDto } from './user.service';

type LoadState = 'loading' | 'success' | 'error';

@Component({
  selector: 'app-user-list',
  standalone: true,
  template: `
    @if (state() === 'loading') { <p role="status">Caricamento…</p> }
    @if (state() === 'error') { <p role="alert">Impossibile caricare gli utenti.</p> }
    @if (state() === 'success') {
      <ul>
        @for (user of users(); track user.id) { <li>{{ user.name }}</li> }
        @empty { <li>Nessun utente presente.</li> }
      </ul>
    }
  `
})
export class UserListComponent implements OnInit {
  private readonly userService = inject(UserService);
  readonly state = signal<LoadState>('loading');
  readonly users = signal<UserDto[]>([]);

  ngOnInit(): void {
    this.userService.list().subscribe({
      next: users => { this.users.set(users); this.state.set('success'); },
      error: () => this.state.set('error')
    });
  }
}
```

Il tipo generico aiuta il compilatore, ma non convalida il JSON a runtime. Il serializer web di ASP.NET Core rende normalmente `Id` e `Name` come `id` e `name`; client e server devono accordarsi su path, status, nomi e forme dei dati. OpenAPI o test di contratto possono rendere verificabile quell'accordo. In sviluppo, usa un proxy oppure configura CORS se le origini differiscono.

## Dal click al database e ritorno

```text
GET /api/users → JSON 200 → Observable<UserDto[]> → stato del componente → template
```

### Racconta l'operazione dal file al risultato

1. Il componente chiama `UserService.list()`; il service restituisce l'Observable di `HttpClient`, che descrive la richiesta.
2. Quando il componente si sottoscrive, il browser invia `GET /api/users` al processo ASP.NET Core. Un proxy può inoltrare l'origine locale; altrimenti il browser applica la policy CORS.
3. Il route handler usa il `DbContext`, EF Core interroga SQLite, proietta righe in `UserResponse` e ASP.NET Core serializza il DTO in JSON con status `200`.
4. Il client riceve il JSON e aggiorna loading/success/error. Se il server rinomina `Name` senza adeguare il contratto, TypeScript non corregge la risposta: osserva il payload nel pannello Network e aggiorna DTO o API in modo coordinato.

Il laboratorio Monorepo completa la GET in `SubjectsService`, poi aggiunge form e azioni UI per il CRUD. Prova un ciclo dal browser: i test separati di client e server non dimostrano da soli che entrambi i processi comunichino.

## Trova il primo punto in cui il dato cambia forma

- Dare per scontato che il monorepo condivida automaticamente tipi o dipendenze
- mantenere i manifest nei progetti corretti e verificare il contratto HTTP tra client e server.

> **Quale processo possiede ciascun passaggio?** Quale vantaggio pratico offre un Monorepo per il rilascio congiunto di modifiche a client e server?

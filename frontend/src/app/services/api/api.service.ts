import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, throwError } from 'rxjs';
import { catchError, retry } from 'rxjs/operators';

interface Usuario {
  username: string;
  email: string;
  password: string;
}

interface UsuarioAuth {
  username: string;
  password: string;
}

interface Token {
  token: string;
}

@Injectable({
  providedIn: 'root',
})
export class ApiService {
  private baseUrl = 'http://localhost:8000';

  constructor(private http: HttpClient) {}

  login(usuario: UsuarioAuth): Observable<Token> {
    return this.http.post<Token>(`${this.baseUrl}/login/`, usuario);
  }

  cadastraUsuario(usuario: Usuario): Observable<Usuario> {
    return this.http.post<Usuario>(`${this.baseUrl}/users/`, usuario);
  }
}

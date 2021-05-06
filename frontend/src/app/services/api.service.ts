import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, throwError } from 'rxjs';
import { catchError, retry } from 'rxjs/operators';

interface Usuario {
  username: string;
  email: string;
  password: string;
}
@Injectable({
  providedIn: 'root',
})
export class ApiService {
  private baseUrl = ' http://localhost:8000/users';

  constructor(private http: HttpClient) {}

  cadastraUsuario(usuario: Usuario): Observable<Usuario> {
    return this.http.post<Usuario>(`${this.baseUrl}/users/`, usuario);
  }
}

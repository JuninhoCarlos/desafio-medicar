import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class AuthService {
  constructor() {}

  setLogin(usuario: string, token: string): void {
    localStorage.setItem('usuario', usuario);
    localStorage.setItem('token', token);
  }

  isLogged(): boolean {
    return localStorage.getItem('token') ? true : false;
  }

  logout(): void {
    localStorage.clear();
  }
}

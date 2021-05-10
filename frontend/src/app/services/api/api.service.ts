import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
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

  private getHeader(): HttpHeaders {
    const token = localStorage.getItem('token');
    const header = new HttpHeaders({ Authorization: `Token ${token}` });
    return header;
  }

  login(usuario: UsuarioAuth): Observable<Token> {
    return this.http.post<Token>(`${this.baseUrl}/login/`, usuario);
  }

  cadastraUsuario(usuario: Usuario): Observable<Usuario> {
    return this.http.post<Usuario>(`${this.baseUrl}/users/`, usuario);
  }

  getEspecialidades(): Observable<Array<object>> {
    const header = this.getHeader();
    return this.http.get<Array<object>>(`${this.baseUrl}/especialidades/`, {
      headers: header,
    });
  }

  getMedicosPorEspecialidade(
    especialidadeId: string
  ): Observable<Array<object>> {
    return this.http.get<Array<object>>(
      `${this.baseUrl}/medicos/?especialidade=${especialidadeId}`,
      {
        headers: this.getHeader(),
      }
    );
  }

  getAgendasDoMedico(medicoID: string): Observable<Array<any>> {
    return this.http.get<Array<any>>(
      `${this.baseUrl}/agendas/?medico=${medicoID}`,
      {
        headers: this.getHeader(),
      }
    );
  }

  getAgendaDoDiaDoMedico(medicoID: string, dia: string): Observable<any> {
    return this.http.get<any>(
      `${this.baseUrl}/agendas/?medico=${medicoID}&data_inicio=${dia}&data_final=${dia}`,
      {
        headers: this.getHeader(),
      }
    );
  }

  cadastraConsulta(agendaId: Number, horario: string): Observable<any> {
    let data = {
      agenda_id: agendaId,
      horario: horario,
    };
    return this.http.post<any>(`${this.baseUrl}/consultas/`, data, {
      headers: this.getHeader(),
    });
  }

  getConsultas() {
    return this.http.get<any>(`${this.baseUrl}/consultas/`, {
      headers: this.getHeader(),
    });
  }

  desmarcarConsulta(consultaId: Number) {
    return this.http.delete<any>(`${this.baseUrl}/consultas/${consultaId}/`, {
      headers: this.getHeader(),
    });
  }
}

import { Component, OnInit } from '@angular/core';
import {
  FormBuilder,
  FormGroup,
  FormsModule,
  Validators,
} from '@angular/forms';
import { Router } from '@angular/router';

import { ApiService } from 'src/app/services/api';
import { AuthService } from '../../services/auth';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css'],
})
export class LoginComponent implements OnInit {
  form: FormGroup;
  constructor(
    private fb: FormBuilder,
    private authService: AuthService,
    private api: ApiService,
    private router: Router
  ) {
    this.form = this.fb.group({
      nome: ['', Validators.required],
      password: ['', [Validators.required]],
    });
  }

  onSubmit(): void {
    let user = {
      username: this.form.get('nome')?.value,
      password: this.form.get('password')?.value,
    };

    this.api.login(user).subscribe(
      (data) => {
        this.authService.setLogin(user.username, data.token);
        this.router.navigate(['']);
      },
      (errors) => {
        this.form.reset();
        this.form.setErrors({ autenticacao: true });
      }
    );
  }

  ngOnInit(): void {
    if (this.authService.isLogged()) {
      this.router.navigate(['home']);
    }
  }
}

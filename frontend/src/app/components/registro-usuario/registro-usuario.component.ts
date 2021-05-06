import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Router } from '@angular/router';

import { senhaValidator } from '../utils/validators';
import { ApiService } from '../../services/api.service';

@Component({
  selector: 'app-registro-usuario',
  templateUrl: './registro-usuario.component.html',
  styleUrls: ['./registro-usuario.component.css'],
})
export class RegistroUsuarioComponent implements OnInit {
  form: FormGroup;

  constructor(
    private fb: FormBuilder,
    private api: ApiService,
    private router: Router
  ) {
    this.form = this.fb.group(
      {
        nome: ['', Validators.required],
        email: [
          '',
          {
            validators: [Validators.required, Validators.email],
            updateOn: 'blur',
          },
        ],
        password: ['', [Validators.required]],
        password2: ['', [Validators.required]],
      },
      { validators: senhaValidator, updateOn: 'blur' }
    );
  }

  ngOnInit(): void {}
  onSubmit(): void {
    let usuario = {
      username: this.form.get('nome')?.value,
      email: this.form.get('email')?.value,
      password: this.form.get('password')?.value,
    };

    this.api.cadastraUsuario(usuario).subscribe(
      (data) => {
        this.router.navigate(['']);
      },
      (errors) => {
        this.form.reset();
        this.form.setErrors({ request: true });
      }
    );
  }
}

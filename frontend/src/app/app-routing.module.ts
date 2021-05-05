import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

import { RegistroUsuarioComponent } from "./components/registro-usuario/registro-usuario.component"
import { LoginComponent } from "./components/login/login.component"

const routes: Routes = [
  { path: '', component: LoginComponent },
  { path: 'registro-usuario', component: RegistroUsuarioComponent },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }

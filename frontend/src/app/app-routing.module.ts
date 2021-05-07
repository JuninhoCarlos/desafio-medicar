import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

import { RegistroUsuarioComponent } from './components/registro-usuario';
import { LoginComponent } from './components/login';
import { HomeComponent } from './components/home';

import { LoggedInGuard } from './logged-in.guard';

const routes: Routes = [
  { path: '', redirectTo: 'home', pathMatch: 'full' },
  { path: 'login', component: LoginComponent },
  { path: 'registro-usuario', component: RegistroUsuarioComponent },
  { path: 'home', component: HomeComponent, canActivate: [LoggedInGuard] },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule],
})
export class AppRoutingModule {}

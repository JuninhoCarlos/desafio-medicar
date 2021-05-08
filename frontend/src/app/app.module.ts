import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { HttpClientModule } from '@angular/common/http';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { LoginComponent } from './components/login';
import { RegistroUsuarioComponent } from './components/registro-usuario';

import { ApiService } from './services/api';
import { HomeComponent } from './components/home';
import { LoggedInGuard } from './logged-in.guard';
import { HeaderComponent } from './components/header/header.component';
import { ListaConsultasComponent } from './components/lista-consultas/lista-consultas.component';
import { ModalComponent } from './components/modal/modal.component';
import { NoopAnimationsModule } from '@angular/platform-browser/animations';

@NgModule({
  declarations: [
    AppComponent,
    LoginComponent,
    RegistroUsuarioComponent,
    HomeComponent,
    HeaderComponent,
    ListaConsultasComponent,
    ModalComponent,
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    FormsModule,
    ReactiveFormsModule,
    HttpClientModule,
    NoopAnimationsModule,
  ],
  providers: [ApiService, LoggedInGuard],
  bootstrap: [AppComponent],
})
export class AppModule {}

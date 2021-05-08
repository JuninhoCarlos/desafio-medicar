import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-lista-consultas',
  templateUrl: './lista-consultas.component.html',
  styleUrls: ['./lista-consultas.component.css'],
})
export class ListaConsultasComponent implements OnInit {
  showModal: boolean;
  constructor() {
    this.showModal = false;
  }

  ngOnInit(): void {}

  toggleShowModal() {
    this.showModal = !this.showModal;
  }

  onClose() {
    this.showModal = false;
  }
}

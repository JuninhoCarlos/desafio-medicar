import { Component, OnInit } from '@angular/core';

import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { ApiService } from '../../services/api';

@Component({
  selector: 'app-lista-consultas',
  templateUrl: './lista-consultas.component.html',
  styleUrls: ['./lista-consultas.component.css'],
})
export class ListaConsultasComponent implements OnInit {
  showModal: boolean;
  form: FormGroup;

  especialidades!: Array<any>;
  medicos!: Array<any>;
  datas!: Array<string>;
  horarios!: Array<string>;

  consultas!: Array<any>;

  private agendaId!: Number;

  constructor(private fb: FormBuilder, private api: ApiService) {
    this.form = this.fb.group({
      especialidade: [null, Validators.required],
      medico: [null, Validators.required],
      data: [null, Validators.required],
      hora: [null, Validators.required],
    });
    this.showModal = false;
  }

  ngOnInit(): void {
    this.api.getEspecialidades().subscribe((data) => {
      this.especialidades = data;
    });

    this.api.getConsultas().subscribe((data) => {
      console.log(data);
      this.consultas = data;
    });
  }

  onEspecialidadeChange(idEspecialidade: string) {
    this.api.getMedicosPorEspecialidade(idEspecialidade).subscribe((data) => {
      this.medicos = data;
    });
  }

  onMedicoChange(idMedico: string) {
    this.api.getAgendasDoMedico(idMedico).subscribe((response) => {
      this.datas = response.map((agenda) => {
        return agenda.dia;
      });
    });
  }

  onDataChange(data: string) {
    this.api
      .getAgendaDoDiaDoMedico(this.form.get('medico')?.value, data)
      .subscribe((data) => {
        data.forEach((agenda: any) => {
          console.log('horarios desse dia', agenda.horarios);
          this.agendaId = agenda.id;
          this.horarios = agenda.horarios;
        });
      });
  }

  desmarcarConsulta(consultaId: Number) {
    console.log('desmarcar consulta', consultaId);
    this.api.desmarcarConsulta(consultaId).subscribe((data) => {
      this.consultas = this.consultas.filter((consulta) => {
        return consulta.id != consultaId;
      });
    });
  }

  toggleShowModal() {
    this.showModal = !this.showModal;
  }

  onClose() {
    this.showModal = false;
  }

  onSubmit() {
    //console.log('Agenda id: ', this.agendaId);
    //console.log('horario', this.form.get('hora')?.value);
    this.api
      .cadastraConsulta(this.agendaId, this.form.get('hora')?.value)
      .subscribe((data) => {
        this.consultas.push(data);
        this.form.reset();
        this.showModal = false;
      });
  }
}

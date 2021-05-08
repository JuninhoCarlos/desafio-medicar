import {
  Component,
  OnInit,
  Input,
  Output,
  EventEmitter,
  ElementRef,
  Directive,
  ViewChild,
  AfterContentInit,
  ContentChildren,
  AfterViewInit,
  QueryList,
} from '@angular/core';

@Component({
  selector: 'app-modal[display]',
  templateUrl: './modal.component.html',
  styleUrls: ['./modal.component.css'],
})
export class ModalComponent implements OnInit, AfterViewInit {
  @Input() display?: boolean;
  /*
  get display(): boolean {
    return this._display;
  }
  set display(display: boolean) {
    console.log('update from parent');
    this._display = display;
  }
  private _display = false;
  */
  @Output() onClose = new EventEmitter();

  constructor() {}

  ngOnInit(): void {
    //console.log('init', this.child);
  }
  ngAfterViewInit() {
    console.log('After view init');
  }
}

import { Component, Input } from '@angular/core';

@Component({
  selector: 'app-feedback-accordian',
  templateUrl: './feedback-accordian.component.html',
  styleUrl: './feedback-accordian.component.css'
})
export class FeedbackAccordianComponent {
  @Input() emp_data : any;
  @Input() index  : number ;
  isCollapsed: boolean[] = [];

  toggleIcon(index: number) {
    this.isCollapsed[index] = !this.isCollapsed[index];
  }
}

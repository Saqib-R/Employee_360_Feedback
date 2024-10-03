import { Router, RouterModule } from '@angular/router';
import { SharedService } from './../../services/shared.service';
import { Component, EventEmitter, inject, Input, Output } from '@angular/core';

@Component({
  selector: 'app-feedback-accordian',
  templateUrl: './feedback-accordian.component.html',
  styleUrl: './feedback-accordian.component.css'
})
export class FeedbackAccordianComponent {
  @Input() emp_data : any;
  @Input() index  : number ;
  isCollapsed: boolean[] = [];
  sharedService : SharedService = inject(SharedService);
  router : Router = inject(Router);



  toggleIcon(index: number) {
    this.isCollapsed[index] = !this.isCollapsed[index];
  }

  sendData(data,question) {
    this.sharedService.empData(data);
    this.sharedService.queNo(question);
    this.router.navigate(['/home/summarisation'])
  }
}

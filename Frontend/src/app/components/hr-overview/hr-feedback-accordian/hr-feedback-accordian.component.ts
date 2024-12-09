import { Component, inject, Input } from '@angular/core';
import { Router } from '@angular/router';
import { SharedService } from '../../../services/shared.service';
import { EmployeeServiceService } from '../../../services/employee-data.service';

@Component({
  selector: 'app-hr-feedback-accordian',
  templateUrl: './hr-feedback-accordian.component.html',
  styleUrl: './hr-feedback-accordian.component.css'
})
export class HrFeedbackAccordianComponent {
  @Input() emp_data : any;
  @Input() index  : number ;
  router : Router = inject(Router);
  employeeService : EmployeeServiceService = inject(EmployeeServiceService);
  isCollapsed: boolean[] = [];

  toggleIcon(index: number) {
    this.isCollapsed[index] = !this.isCollapsed[index];
  }

  goToEmployeeDetail(id: number) {
    this.employeeService.setEmployeeData(this.emp_data);
    this.router.navigate(['/hr-employee', id]);
  }


}

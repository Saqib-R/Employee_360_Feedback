import { Component, inject } from '@angular/core';
import { EmployeeServiceService } from '../../services/employee-data.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-emp-accordian-card',
  templateUrl: './emp-accordian-card.component.html',
  styleUrl: './emp-accordian-card.component.css'
})
export class EmpAccordianCardComponent {

  private employeeService: EmployeeServiceService = inject(EmployeeServiceService)
  router : Router = inject(Router);
  employee : any = null;

  ngOnInit() {
    this.employee = this.employeeService.getEmployeeData();
  }

  goBack() {
    this.router.navigate(['employee-overview']);
  }
}

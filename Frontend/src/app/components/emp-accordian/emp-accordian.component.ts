import { Component, inject, Input } from '@angular/core';
import { SharedService } from '../../services/shared.service';
import { Router } from '@angular/router';
import { EmployeeServiceService } from '../../services/employee-data.service';

@Component({
  selector: 'app-emp-accordian',
  templateUrl: './emp-accordian.component.html',
  styleUrl: './emp-accordian.component.css'
})
export class EmpAccordianComponent {
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
    this.router.navigate(['/employee', id]);
  }
}

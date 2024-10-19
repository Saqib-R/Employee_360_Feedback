import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class EmployeeServiceService {

  constructor() { }

  private employeeData: any;

  setEmployeeData(data: any) {
    this.employeeData = data;
  }

  getEmployeeData() {
    return this.employeeData;
  }

}

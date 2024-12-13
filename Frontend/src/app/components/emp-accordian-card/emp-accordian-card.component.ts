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
  attributeQ1 = [];
  attributeQ2 = [];
  attributeQ3 = [];
  attributeQ4 = [];
  showChatbot = false;

  toggleChatbot() {
    this.showChatbot = !this.showChatbot;
  }

  ngOnInit() {
    this.employee = this.employeeService.getEmployeeData();
    // if(this.employee) {

    //   this.attributeQ1 = this.parseFeedbackText(this.employee?.expSumm?.question1);
    //   this.attributeQ2 = this.parseFeedbackText(this.employee?.expSumm?.question2);
    //   this.attributeQ3 = this.parseFeedbackText(this.employee?.expSumm?.question3);
    //   this.attributeQ4 = this.parseFeedbackText(this.employee?.expSumm?.question4);

    // }
  }

  goBack() {
    this.router.navigate(['employee-overview']);
  }



  // parseFeedbackText(text: string) {
  //   // Use regex to split by headings and capture content
  //   const sections = text.split(/(?<=\*\*)\s*|\*\*\s*/).filter(Boolean);

  //   const parsedAttributes = [];
  //   for (let i = 0; i < sections.length; i++) {
  //     if (i % 2 === 0) { // This is the heading
  //       parsedAttributes.push({
  //         attribute: sections[i].trim().replace(/\*\*/g, ''), // Remove asterisks
  //         content: sections[i + 1] ? sections[i + 1].trim() : '' // Get the next item as content
  //       });
  //     }
  //   }
  //   console.log(parsedAttributes);

  //   return parsedAttributes;
  // }



}

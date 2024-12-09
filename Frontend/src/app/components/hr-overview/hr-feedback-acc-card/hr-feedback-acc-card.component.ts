import { Component, inject } from '@angular/core';
import { Router } from '@angular/router';
import { EmployeeServiceService } from '../../../services/employee-data.service';
import { UploadService } from '../../../services/upload.service';
import { ToastrService } from 'ngx-toastr';
import { SharedService } from '../../../services/shared.service';

@Component({
  selector: 'app-hr-feedback-acc-card',
  templateUrl: './hr-feedback-acc-card.component.html',
  styleUrl: './hr-feedback-acc-card.component.css'
})
export class HrFeedbackAccCardComponent {

  private employeeService: EmployeeServiceService = inject(EmployeeServiceService)
  private uploadService: UploadService = inject(UploadService)
  private sharedService: SharedService = inject(SharedService)
  router : Router = inject(Router);
  toastr: ToastrService = inject(ToastrService)
  employee : any = null;
  attributeQ1 = [];
  attributeQ2 = [];
  attributeQ3 = [];
  attributeQ4 = [];

  ngOnInit() {
    this.employee = this.employeeService.getEmployeeData();
    console.log(this.employee);

    // if(this.employee) {

    //   this.attributeQ1 = this.parseFeedbackText(this.employee?.expSumm?.question1);
    //   this.attributeQ2 = this.parseFeedbackText(this.employee?.expSumm?.question2);
    //   this.attributeQ3 = this.parseFeedbackText(this.employee?.expSumm?.question3);
    //   this.attributeQ4 = this.parseFeedbackText(this.employee?.expSumm?.question4);
    // }
  }

  goBack() {
    this.router.navigate(['/home/hr-feedback-overview']);
  }

  approveFeedback() {
    if(this.employee){
      const empDetail = {
        subject: this.employee?.subject,
        job_title: this.employee?.job_title,
        manager: this.employee?.manager,
        function_code: this.employee?.function_code,
        level: this.employee?.level,
        emp_id: this.employee?.emp_id,
        status : this.employee?.status
      }

      console.log(empDetail);


      this.uploadService.approveSummary( empDetail, this.employee.summary).subscribe({
        next: (res) => {
          console.log(res);
              this.employee.status = 'approved'
              this.toastr.success('Response Generated', 'Success...👍', {
                  timeOut: 50000,
              });
              this.router.navigate(['/home/hr-feedback-overview']);

          },
          error: (err) => {
              console.error(err);
          }
      });
    }
  }

  regenerateSummary(data,question) {
    if(question === "all") {
      const allFeedback = [
        ...data.questions?.question1,
        ...data.questions?.question2,
        ...data.questions?.question3,
        ...data.questions?.question4
      ];

      // Adding the concatenated feedback to a new key 'all'
      data.all = allFeedback;
      const empData = {
        subject: this.employee?.subject,
        job_title: this.employee?.job_title,
        manager: this.employee?.manager,
        function_code: this.employee?.function_code,
        level: this.employee?.level,
        emp_id: this.employee?.emp_id,
        question1 : [...data.questions?.question1],
        question2 : [...data.questions?.question2],
        question3 : [...data.questions?.question3],
        question4 : [...data.questions?.question4]
      }
      this.sharedService.empData(empData);
      this.sharedService.queNo(question);
      this.router.navigate(['/home/summarisation'])
    }
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

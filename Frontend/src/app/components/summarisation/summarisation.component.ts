import { Component, inject, Input, input } from '@angular/core';
import { SharedService } from '../../services/shared.service';
import { UploadService } from '../../services/upload.service';
import { ToastrService } from 'ngx-toastr';

@Component({
  selector: 'app-summarisation',
  templateUrl: './summarisation.component.html',
  styleUrl: './summarisation.component.css'
})
export class SummarisationComponent {

  feedbackQuestion = {
    'question1' : "Please provide a few examples of this individual's greatest achievements and/or contributions this year from your perspective.",
    'question2': "How has this individual demonstrated CustomerOrg's cultural values, according to the Career Framework? Please provide a few examples.",
    'question3': "What skills or capabilities can this individual build or expand upon that would allow the individual to contribute even more value in the future?",
    'question4': "What skills should this individual focus on developing in the future to progress to the next level (if applicable)? Please refer to the Career Framework to review the expected results and behaviors at the next level."
  };

  question: string = "How does Jane Doe handle complex tasks?";
  summaryResponse: string = "Jane consistently demonstrates strong problem-solving skills in handling complex tasks. Jane consistently demonstrates strong problem-solving skills in handling complex tasks. Jane consistently demonstrates strong problem-solving skills in handling complex tasks";
  promptInput: string = '';
  isCollapsed : boolean = false;
  sharedService : SharedService = inject(SharedService);
  summarizeService : UploadService = inject(UploadService);
  toastr : ToastrService = inject(ToastrService);
  summaries : any;
  data: any;
  questionNo : any;
  loading: boolean ;
  prevName : string = null;
  currName : string = null;
  prevQueNo : string = null;
  currQueNo : string = null;
  


  ngOnInit(): void {
    this.sharedService.employeeData.subscribe(data =>{
      if(this.currName === null) {
        this.prevName = data?.subject;
      }
      this.prevName = this.currName
      this.currName = data?.subject;
      this.data = data;
    } );
    this.sharedService.questionNu.subscribe(question => {
      if(this.currQueNo === null) {
        this.prevQueNo = question;
      }
      this.prevQueNo = this.currQueNo;
      this.currQueNo = question;
      this.questionNo = question;

    });

    

    this.handleSummarization();


    // if(JSON.parse(localStorage.getItem('summary'))) {
    //   this.summaries = JSON.parse(localStorage.getItem('summary'))
    // }else {
    //   if(this?.data?.[this.questionNo]) {
    //     this.loading = true;
    //     this.summarizeService.summarizeFeedback(this?.data?.[this.questionNo]).subscribe({
    //       next : (res) => {
    //         this.toastr.success('Response Generated', 'Success...👍', {
    //           timeOut: 50000,
    //         });
    //         this.loading = false
    //         this.summaries = res?.summaries;
    //         localStorage.setItem('summary', JSON.stringify(res?.summaries));
    //       },
    //       error : (err) => {
    //         console.error(err);
    //         this.loading = false;
    //       }
    //     })
    //   }
    // }   
    
  }

  private handleSummarization(): void {

    console.log(this.questionNo , this.prevQueNo, this.questionNo==this.prevQueNo);
    
    // Clear local storage if the question or employee changes
      if(this.currName === this.prevName && this.currQueNo === this.prevQueNo) {
        console.log("All Ok");
        
      }else {
        localStorage.removeItem('summary')
      }

    // Check if we have a valid summary in local storage
    const storedSummary = JSON.parse(localStorage?.getItem('summary'));
    if (storedSummary) {
        this.summaries = storedSummary;
    } else {
        // If no summary in local storage, make the API call
        if (this?.data?.[this.questionNo]) {
            this.loading = true;
            this.summarizeService.summarizeFeedback(this?.data?.[this.questionNo]).subscribe({
                next: (res) => {
                    this.toastr.success('Response Generated', 'Success...👍', {
                        timeOut: 50000,
                    });
                    this.loading = false;
                    this.summaries = res?.summaries;
                    localStorage.setItem('summary', JSON.stringify(res?.summaries));
                },
                error: (err) => {
                    console.error(err);
                    this.loading = false;
                }
            });
        }
    }
  }

  // Function to handle prompt submission
  submitPrompt() {
    console.log('Prompt submitted: ', this.promptInput);
    // Lama response will get it later
  }

  // Adjusting textarea height dynamically
  adjustTextareaHeight(event: any) {
    const textarea = event.target;
    textarea.style.height = 'auto';
    textarea.style.height = textarea.scrollHeight + 'px';
  }

  // Tracking whether the summary is expanded or not
  isExpanded: boolean = false;
  // Toggle expand/collapse state
  toggleSummary() {
    this.isExpanded = !this.isExpanded;
    const summaryText = document.querySelector('.summary-text');
    const toggleIcon = document.querySelector('.summary-toggle i');
    if (this.isExpanded) {
      summaryText?.setAttribute('style', 'max-height: none');
      toggleIcon?.classList.add('collapsed');
    } else {
      summaryText?.setAttribute('style', 'max-height: 100px');
      toggleIcon?.classList.remove('collapsed');
    }
  }

  toggleIcon() {
    this.isCollapsed = !this.isCollapsed;
  }

}

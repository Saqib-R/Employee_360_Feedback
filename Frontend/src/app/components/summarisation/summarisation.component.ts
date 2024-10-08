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

  feedbackQuestionNo = {
    'question1' : "Question - 1:-",
    'question2': "Question - 2:-",
    'question3': "Question - 3:-",
    'question4': "Question - 4:-"
  };

  promptInput: string = '';
  isCollapsed : boolean = false;
  sharedService : SharedService = inject(SharedService);
  summarizeService : UploadService = inject(UploadService);
  toastr : ToastrService = inject(ToastrService);
  summaries : any;
  isExpanded: boolean = false;
  data: any;
  questionNo : any;
  loading: boolean ;
  currName : string = null;
  currQueNo : string = null;
  prompt: string = '';
  customSummary: string | null = null;


  ngOnInit(): void {


    this.sharedService.employeeData.subscribe(data =>{      
      this.currName = data?.subject;
      this.data = data;
    } );
    this.sharedService.questionNu.subscribe(question => {
      
      this.currQueNo = question;
      this.questionNo = question;
    });

    if(!localStorage.getItem('Name')) {
      localStorage.setItem('Name', this.currName) ;
    }

    if(!localStorage.getItem('QueNo')) {
      localStorage.setItem('QueNo', this.currQueNo) ;
    }

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

    // console.log(this.currQueNo , localStorage.getItem('QueNo'), this.questionNo===localStorage.getItem('QueNo'));
    
    // Clear local storage if the question or employee changes
      if(this.currName === localStorage.getItem('Name') && this.currQueNo === localStorage.getItem('QueNo')) {
        console.log("All Ok");        
      }else {
        localStorage.setItem('Name', this.currName) ;
        localStorage.setItem('QueNo', this.questionNo) ;
        localStorage.removeItem('summary')
        localStorage.removeItem('cusSummary');
      }

    // Check if we have a valid summary in local storage
    const storedSummary = JSON.parse(localStorage?.getItem('summary'));
    const custSummary = localStorage.getItem('cusSummary');
    if (storedSummary) {
        this.summaries = storedSummary;
        this.customSummary = custSummary;
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
    
    if (this?.data?.[this.questionNo].length === 0 || !this.prompt) {
      this.toastr.error('Please provide feedbacks and a prompt.', 'Validation Error');
      return;
    }
    this.summarizeService.customSummarizeFeedback(this?.data?.[this.questionNo], this.prompt).subscribe({
      next: (response) => {
        this.customSummary = response.summary;
        console.log(response);     
        localStorage.setItem("cusSummary", response.summary); 
        this.toastr.success('Summary generated successfully!', 'Success');
      },
      error: (err) => {
        console.error(err);
        this.toastr.error('Failed to generate summary.', 'Error');
      }
    });
  }

  handleKeyDown(event: KeyboardEvent) {
    if (event.key === 'Enter') {
        event.preventDefault(); 
        this.submitPrompt();
        this.prompt = '';
    }
    
  }

  // Adjusting textarea height dynamically
  adjustTextareaHeight(event: any) {
    const textarea = event.target;
    textarea.style.height = 'auto';
    textarea.style.height = textarea.scrollHeight + 'px';
  }

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

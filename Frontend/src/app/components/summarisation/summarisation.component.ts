import { Component, inject, Input, input } from '@angular/core';
import { SharedService } from '../../services/shared.service';
import { UploadService } from '../../services/upload.service';
import { ToastrService } from 'ngx-toastr';

declare var bootstrap: any;

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
    'question4': "Question - 4:-",
    'all': "All question's feedbacks"
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
  GenLoading: boolean ;
  CustLoading: boolean ;
  currName : string = null;
  currQueNo : string = null;
  prompt: string = '';
  customSummary: string | null = null;
  text = '';
  cusText = '';
  expText = ''
  private index = 0;
  isCopied = false;
  ExpSumLoading: boolean ;
  ExpecSummary: any | null = null;
  summaryKeys : any;



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
        localStorage.removeItem('expeSummary')
      }

    // Check if we have a valid summary in local storage
    const storedSummary = JSON.parse(localStorage?.getItem('summary'));
    const custSummary = localStorage.getItem('cusSummary');
    const expecSummary = JSON.parse(localStorage.getItem('expeSummary'));

    if (storedSummary) {
        this.summaries = storedSummary;
        this.text = storedSummary;
        this.customSummary = custSummary;
        this.cusText = custSummary;
        this.ExpecSummary = expecSummary
        console.log("EXPEC SUMMARY FROM LOCAL STORAGE",this.ExpecSummary);
        this.summaryKeys = null;
        this.summaryKeys = Array.from(
          new Map(Object.keys(this.ExpecSummary.summaries).map(key => [key.toLowerCase(), key])).values()
        );
        // this.typeGeneratedSummary();
    } else {
        // If no summary in local storage, make the API call
        if (this?.data?.[this.questionNo]) {
            this.GenLoading = true;
            this.summarizeService.summarizeFeedback(this?.data?.[this.questionNo]).subscribe({
                next: (res) => {
                    this.toastr.success('Response Generated', 'Success...👍', {
                        timeOut: 50000,
                    });
                    console.log(res);

                    this.GenLoading = false;
                    this.summaries = res?.summaries;
                    localStorage.setItem('summary', JSON.stringify(res?.summaries));
                    this.typeGeneratedSummary();
                },
                error: (err) => {
                    console.error(err);
                    this.GenLoading = false;
                }
            });
        }
    }
  }

  // Function to handle prompt submission
  submitPrompt() {
    console.log('Prompt submitted: ', this.prompt);
    if (this?.data?.[this.questionNo].length === 0 || !this.prompt) {
      console.log('Please provide feedbacks and a prompt.', 'Validation Error');
      this.toastr.error('Please provide feedbacks and a prompt.', 'Validation Error');
      return;
    }
    this.CustLoading = true;
    this.summarizeService.customSummarizeFeedback(this?.data?.[this.questionNo], this.prompt).subscribe({
      next: (response) => {
        this.prompt = '';
        this.customSummary = response.summary;
        console.log(response);
        localStorage.setItem("cusSummary", response.summary);
        this.toastr.success('Summary generated successfully!', 'Success');
        this.cusText = '';
        this.CustLoading = false;
        this.typeCusSummary();
      },
      error: (err) => {
        console.error(err);
        this.toastr.error('Failed to generate summary.', 'Error');
        this.CustLoading = false;
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

  reSummarize() {
    if (this?.data?.[this.questionNo]) {
      this.GenLoading = true;
      this.summarizeService.summarizeFeedback(this?.data?.[this.questionNo]).subscribe({
          next: (res) => {
              this.toastr.success('Response Generated', 'Success...👍', {
                  timeOut: 50000,
              });
              this.GenLoading = false;
              this.summaries = res?.summaries;
              localStorage.setItem('summary', JSON.stringify(res?.summaries));
              this.text = '';
              this.typeGeneratedSummary();
          },
          error: (err) => {
              console.error(err);
              this.GenLoading = false;
          }
      });
  }
  }

  private typeGeneratedSummary() {
    for (let i = 0; i < this.summaries[0]?.length; i++) {
        setTimeout(() => {
            this.text += this.summaries[0]?.charAt(i);
        }, i * 20); // Adjust the delay based on the index
    }
  }

  private typeCusSummary() {
      for (let i = 0; i < this.customSummary?.length; i++) {
          setTimeout(() => {
              this.cusText += this.customSummary?.charAt(i);
          }, i * 20); // Adjust the delay based on the index
      }
  }

  private typeExpecSummary() {
      for (let i = 0; i < this.ExpecSummary?.length; i++) {
          setTimeout(() => {
              this.expText += this.ExpecSummary?.charAt(i);
          }, i * 10); // Adjust the delay based on the index
      }
  }

  ngAfterViewInit() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl));
  }

  copyToClipboard(text) {
    if (text) {
      navigator.clipboard.writeText(text).then(() => {
        this.isCopied = true;

        setTimeout(() => {
          this.isCopied = false;
        }, 2000);
      }).catch(err => {
        console.error('Could not copy text: ', err);
      });
    }
  }


  getExpecSummary() {
    if (this?.data?.[this.questionNo].length === 0 ) {
      console.log('Please provide feedbacks .', 'Validation Error');
      this.toastr.error('Something went wrong.', 'Validation Error');
      return;
    }
    this.ExpSumLoading = true;
    this.summarizeService.expSummarizeFeedback(this?.data?.[this.questionNo], this.data?.job_title).subscribe({
      next: (response) => {
        this.ExpecSummary = response;
        console.log(response);
        localStorage.setItem("expeSummary", JSON.stringify(this.ExpecSummary));
        this.summaryKeys = Array.from(
          new Map(Object.keys(this.ExpecSummary.summaries).map(key => [key.toLowerCase(), key])).values()
        );

        this.toastr.success('Summary generated successfully!', 'Success');
        this.expText = '';
        this.ExpSumLoading = false;
        this.typeExpecSummary();
      },
      error: (err) => {
        console.error(err);
        this.toastr.error('Failed to generate summary.', 'Error');
        this.CustLoading = false;
      }
    });
  }

  formatText(text: string): string {
    return text.replace(/\**(.*?)\**/g, '<b class="fw-bold">$1</b>');
  }



}

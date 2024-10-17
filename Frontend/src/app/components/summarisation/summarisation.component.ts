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
  GenLoading: boolean ;
  CustLoading: boolean ;
  currName : string = null;
  currQueNo : string = null;
  prompt: string = '';
  customSummary: string | null = null;
  text = '';
  cusText = '';
  private index = 0;
  isCopied = false;


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
      }

    // Check if we have a valid summary in local storage
    const storedSummary = JSON.parse(localStorage?.getItem('summary'));
    const custSummary = localStorage.getItem('cusSummary');
    if (storedSummary) {
        this.summaries = storedSummary;
        this.text = storedSummary;
        this.customSummary = custSummary;
        this.cusText = custSummary;
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
    for (let i = 0; i < this.summaries[0].length; i++) {
        setTimeout(() => {
            this.text += this.summaries[0].charAt(i);
        }, i * 20); // Adjust the delay based on the index
    }
}

private typeCusSummary() {
    for (let i = 0; i < this.customSummary.length; i++) {
        setTimeout(() => {
            this.cusText += this.customSummary.charAt(i);
        }, i * 20); // Adjust the delay based on the index
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

// showNotification(message: string) {
//   // You can implement a simple notification UI here.
//   const notification = document.createElement('div');
//   notification.innerText = message;
//   notification.className = 'notification';

//   // Style the notification
//   Object.assign(notification.style, {
//     position: 'fixed',
//     bottom: '20px',
//     right: '20px',
//     padding: '10px 20px',
//     backgroundColor: '#007bff',
//     color: '#fff',
//     borderRadius: '5px',
//     transition: 'opacity 0.5s',
//     opacity: 0,
//     zIndex: 1000,
//   });

//   document.body.appendChild(notification);

//   // Show the notification
//   setTimeout(() => {
//     notification.style.opacity = '1';
//   }, 0);

//   // Remove the notification after 2 seconds
//   setTimeout(() => {
//     notification.style.opacity = '0';
//     setTimeout(() => {
//       document.body.removeChild(notification);
//     }, 500);
//   }, 2000);
// }


}

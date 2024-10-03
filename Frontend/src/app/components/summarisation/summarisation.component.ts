import { Component, inject, Input, input } from '@angular/core';
import { SharedService } from '../../services/shared.service';

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
  data: any;
  questionNo : any;


  ngOnInit(): void {
    this.sharedService.employeeData.subscribe(data => this.data = data);
    this.sharedService.questionNu.subscribe(question => this.questionNo = question);
    console.log("Emplpoyee Data\n", this.data, "\nQuestion No\n", this.question);
    console.log("QUESTION", this.feedbackQuestion?.[this.questionNo]);
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

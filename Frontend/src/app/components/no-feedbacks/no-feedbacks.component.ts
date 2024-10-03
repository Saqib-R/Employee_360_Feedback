import { Component, inject } from '@angular/core';
import { Router } from '@angular/router';

@Component({
  selector: 'app-no-feedbacks',
  templateUrl: './no-feedbacks.component.html',
  styleUrl: './no-feedbacks.component.css'
})
export class NoFeedbacksComponent {
  router : Router = inject(Router);

  goBackToFeedbacks() {
    this.router.navigate(['/home/upload-csv']);
  }
}

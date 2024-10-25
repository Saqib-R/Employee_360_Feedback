import { Component, Input } from '@angular/core';

@Component({
  selector: 'app-expectation-summary',
  templateUrl: './expectation-summary.component.html',
  styleUrl: './expectation-summary.component.css'
})
export class ExpectationSummaryComponent {
  @Input() key : any;
  @Input() summary : any;
  @Input() rating : any;
  expText = '';


  getStars(rating: number): boolean[] {
    return Array(5).fill(false).map((_, i) => i < rating);
  }

  ngOnInit(): void {
    //Called after the constructor, initializing input properties, and the first call to ngOnChanges.
    //Add 'implements OnInit' to the class.
    this.typeExpecSummary()
  }


  private typeExpecSummary() {
        for (let i = 0; i < this.summary?.length; i++) {
            setTimeout(() => {
                this.expText += this.summary?.charAt(i);
            }, i * 10);
        }
    }
}

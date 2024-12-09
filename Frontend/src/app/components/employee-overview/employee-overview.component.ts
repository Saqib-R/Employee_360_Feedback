import { Component, inject } from '@angular/core';
import { UploadService } from '../../services/upload.service';
import { ToastrService } from 'ngx-toastr';

@Component({
  selector: 'app-employee-overview',
  templateUrl: './employee-overview.component.html',
  styleUrl: './employee-overview.component.css'
})
export class EmployeeOverviewComponent {
  uploadService: UploadService = inject(UploadService);
  toastr : ToastrService = inject(ToastrService);
  summCsvData: any[] | null = null;
  displayedData: any[] | null = null;
  feedbackData : any[] | null = null;
  searchTerm: string = '';
  isLoading : boolean;
  concatenatedResults: any[] = [];


  ngOnInit(): void {
    const conRes = JSON.parse(localStorage.getItem('concatenatedResults'));
    if(conRes && conRes.length > 0) {
      this.concatenatedResults = conRes;
      this.displayedData = conRes;
    }
    else{
      this.uploadService.getEmpSummarizedOverview().subscribe({
        next: (res) => {
          setTimeout(() => {
            this.toastr.success('Data Fetched Successfully', 'Success...👍', {
              timeOut: 5000,
            });
          }, 10);

          this.summCsvData = res.data;
          console.log("SUMMARIZED DATA.....",res);

          // Now call the second API
          this.uploadService.getAllFeedbacks().subscribe({
            next: (res) => {
              this.feedbackData = res;
              console.log("FEEDBACK DARA....",res);

              this.concatenateData(this.summCsvData, this.feedbackData);
              this.displayedData = this.concatenatedResults;
              localStorage.setItem('concatenatedResults', JSON.stringify(this.concatenatedResults));

            },
            error: (err) => {
              console.error(err);
              setTimeout(() => {
                this.toastr.error('Failed to fetch additional data', 'Error...👎', {
                  timeOut: 5000,
                });
              }, 10);
            }
          });
        },
        error: (err) => {
          console.error(err);
          setTimeout(() => {
            this.toastr.error('Failed to fetch employees data', 'Error...👎', {
              timeOut: 5000,
            });
          }, 10);
        }
      });
    }

  }

  concatenateData(firstApiResponse: any[], secondApiResponse: any[]): void {
    // Create a map for the second API response using emp_id for quick lookup
    const secondApiMap = secondApiResponse.reduce((acc, curr) => {
      acc[curr.emp_id] = curr; // Store the entire employee object
      return acc;
    }, {});

    // Combine data from both responses based on emp_id
    this.concatenatedResults = firstApiResponse.map(firstItem => {
      const secondItem = secondApiMap[firstItem.emp_id]; // Look up by emp_id

      // Create a new object that combines relevant information
      return {
        emp_id: firstItem.emp_id,
        function_code: firstItem.function_code,
        job_title: firstItem.job_title,
        level: firstItem.level,
        status: firstItem.status,
        manager: firstItem.manager,
        subject: firstItem ? firstItem.subject : 'N/A', // Get subject from second API
        summary : firstItem.summary || 'N/A',
        questions: {
          question1: secondItem ? secondItem.question1 : ['N/A'],
          question2: secondItem ? secondItem.question2 : ['N/A'],
          question3: secondItem ? secondItem.question3 : ['N/A'],
          question4: secondItem ? secondItem.question4 : ['N/A'],
        },
      };
    });

    console.log('Concatenated Results:', this.concatenatedResults); // Log final results
  }

  onSearchChange() {
    const term = this.searchTerm.toLowerCase();
    // console.log("DATA\n", this.summCsvData, "\nTERM\n", term);

    if (this.summCsvData) {
        this.displayedData = this.concatenatedResults.filter(employee =>
            employee.subject.toLowerCase().includes(term) ||
            employee.function_code.toLowerCase().includes(term) ||
            employee.job_title.toLowerCase().includes(term) ||
            employee.level.toLowerCase().includes(term)
        );

        if (term === '') {
            this.displayedData = this.summCsvData;
        }
    }
    // console.log(this.displayedData);
}
}

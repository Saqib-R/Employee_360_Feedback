import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { HomeComponent } from './components/home/home.component';
import { ViewFeedbacksComponent } from './components/view-feedbacks/view-feedbacks.component';
import { UploadCSVComponent } from './components/upload-csv/upload-csv.component';
import { SummarisationComponent } from './components/summarisation/summarisation.component';
import { BatchSummarizationComponent } from './components/batch-summarization/batch-summarization.component';
import { LoginComponent } from './components/login/login.component';
import { EmployeeOverviewComponent } from './components/employee-overview/employee-overview.component';
import { EmpAccordianCardComponent } from './components/emp-accordian-card/emp-accordian-card.component';

const routes: Routes = [
  { path: '', redirectTo: '/login', pathMatch: 'full' },
  {path: "home", component : HomeComponent},
  {path: "login", component : LoginComponent},
  {path: 'employee-overview', component: EmployeeOverviewComponent},
  { path: 'employee/:id', component: EmpAccordianCardComponent },

  {
    path: 'home',
    component: HomeComponent,
    children: [
      { path: '', redirectTo: 'dashboard', pathMatch: 'full' },
      { path: 'view-feedbacks', component: ViewFeedbacksComponent },
      { path: 'summarisation', component: SummarisationComponent },
      { path: 'batch-summarisation', component: BatchSummarizationComponent },
      { path: 'upload-csv', component: UploadCSVComponent },
    ]
  },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }

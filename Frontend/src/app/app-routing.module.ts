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
import { HrFeedbackOverviewComponent } from './components/hr-overview/hr-feedback-overview/hr-feedback-overview.component';
import { HrFeedbackAccCardComponent } from './components/hr-overview/hr-feedback-acc-card/hr-feedback-acc-card.component';
import { ExpConfigComponent } from './components/exp-config/exp-config.component';
import { ChatBotComponent } from './components/chat-bot/chat-bot.component';

const routes: Routes = [
  { path: '', redirectTo: '/login', pathMatch: 'full' },
  {path: "home", component : HomeComponent},
  {path: "login", component : LoginComponent},
  {path: 'employee-overview', component: EmployeeOverviewComponent},
  { path: 'employee/:id', component: EmpAccordianCardComponent },
  { path: 'hr-employee/:id', component: HrFeedbackAccCardComponent },

  {
    path: 'home',
    component: HomeComponent,
    children: [
      { path: '', redirectTo: 'dashboard', pathMatch: 'full' },
      { path: 'view-feedbacks', component: ViewFeedbacksComponent },
      { path: 'summarisation', component: SummarisationComponent },
      { path: 'batch-summarisation', component: BatchSummarizationComponent },
      {path: 'hr-feedback-overview', component: HrFeedbackOverviewComponent},
      { path: 'upload-csv', component: UploadCSVComponent },
      { path: 'config', component: ExpConfigComponent },
      // { path: 'chat', component: ChatBotComponent },
    ]
  },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }

import { API_URL } from '../../environments/environment';

const BASE_URL : string = API_URL;

// ENDPOINTS
export const endpoints = {
    VIEW_FEEDBACK_API: BASE_URL + "upload",
    VIEW_SUMMARY_API: BASE_URL + "summarize",
    EXPORT_SUMMARY_API: BASE_URL + "upload_feedback",
    DOWNLOAD_SUMMARY_CSV_API: BASE_URL + "download_feedback",
}

/* Instruments */
import {
  apiKeyAddSlice,
  apiKeyListSlice,
  dataFileAddSlice,
  dataFileListSlice,
  flowAddSlice,
  flowDetailSlice,
  flowListSlice,
  flowUpdateSlice,
  jobDetailSlice,
  stripeCheckoutSlice,
  toolAddSlice,
  toolDetailSlice,
  toolListSlice,
  transactionsSummarySlice,
  userSlice,
} from "./slices";

export const reducer = {
  user: userSlice.reducer,
  dataFileAdd: dataFileAddSlice.reducer,
  dataFileList: dataFileListSlice.reducer,
  toolAdd: toolAddSlice.reducer,
  toolList: toolListSlice.reducer,
  toolDetail: toolDetailSlice.reducer,
  flowAdd: flowAddSlice.reducer,
  flowList: flowListSlice.reducer,
  flowDetail: flowDetailSlice.reducer,
  flowUpdate: flowUpdateSlice.reducer,
  jobDetail: jobDetailSlice.reducer,
  apiKeyAdd: apiKeyAddSlice.reducer,
  apiKeyList: apiKeyListSlice.reducer,
  stripeCheckout: stripeCheckoutSlice.reducer,
  transactionsSummary: transactionsSummarySlice.reducer,
};

function varargout = MosaicMaster(varargin)
% MosaicMaster MATLAB code for MosaicMaster.fig
%      MosaicMaster, by itself, creates a new MosaicMaster or raises the existing
%      singleton*.
%
%      H = MosaicMaster returns the handle to a new MosaicMaster or the handle to
%      the existing singleton*.
%
%      MosaicMaster('CALLBACK',hObject,eventData,handles,...) calls the local
%      function named CALLBACK in MosaicMaster.M with the given input arguments.
%
%      MosaicMaster('Property','Value',...) creates a new MosaicMaster or raises the
%      existing singleton*.  Starting from the left, property value pairs are
%      applied to the GUI before MosaicMaster_OpeningFcn gets called.  An
%      unrecognized property name or invalid value makes property application
%      stop.  All inputs are passed to MosaicMaster_OpeningFcn via varargin.
%
%      *See GUI Options on GUIDE's Tools menu.  Choose "GUI allows only one
%      instance to run (singleton)".
%
% See also: GUIDE, GUIDATA, GUIHANDLES

% Edit the above text to modify the response to help MosaicMaster

% Last Modified by GUIDE v2.5 31-Oct-2016 14:40:31

% Begin initialization code - DO NOT EDIT
gui_Singleton = 1;
gui_State = struct('gui_Name',       mfilename, ...
                   'gui_Singleton',  gui_Singleton, ...
                   'gui_OpeningFcn', @MosaicMaster_OpeningFcn, ...
                   'gui_OutputFcn',  @MosaicMaster_OutputFcn, ...
                   'gui_LayoutFcn',  [] , ...
                   'gui_Callback',   []);
if nargin && ischar(varargin{1})
    gui_State.gui_Callback = str2func(varargin{1});
end

if nargout
    [varargout{1:nargout}] = gui_mainfcn(gui_State, varargin{:});
else
    gui_mainfcn(gui_State, varargin{:});
end
% End initialization code - DO NOT EDIT

% --- Executes just before MosaicMaster is made visible.
function MosaicMaster_OpeningFcn(hObject, eventdata, handles, varargin)
% This function has no output args, see OutputFcn.
% hObject    handle to figure
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
% varargin   command line arguments to MosaicMaster (see VARARGIN)
% Read in a reza's color logo image.
% Prepare the full file name.

folder = pwd;
filename = '/logo.png';

A = imread(strcat(folder,filename));
axes(handles.axes);
imshow(A);

% Choose default command line output for MosaicMaster
handles.output = hObject;

% Update handles structure
guidata(hObject, handles);

% UIWAIT makes MosaicMaster wait for user response (see UIRESUME)
% uiwait(handles.figure1);


% --- Outputs from this function are returned to the command line.
function varargout = MosaicMaster_OutputFcn(hObject, eventdata, handles) 
% varargout  cell array for returning output args (see VARARGOUT);
% hObject    handle to figure
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Get default command line output from handles structure
varargout{1} = handles.output;





function edit_text_Callback(hObject, eventdata, handles)
% hObject    handle to edit_text (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of edit_text as text
%        str2double(get(hObject,'String')) returns contents of edit_text as a double


% --- Executes during object creation, after setting all properties.
function edit_text_CreateFcn(hObject, eventdata, handles)
% hObject    handle to edit_text (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end


% --- Executes on button press in start_button.
function start_button_Callback(hObject, eventdata, handles)
 x = get(handles.edit_text,'String'); %edit1 being Tag of ur edit box
 if isempty(x)
    fprintf('Error: Enter Text first\n');
 else
    filename = handles.filename;
    compute_mosaic( str2num(x), filename);
 end
% hObject    handle to start_button (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)


% --- Executes on button press in target_button.
function target_button_Callback(hObject, eventdata, handles)
startingFolder = '.';
defaultFileName = fullfile(startingFolder, '*.*');
[baseFileName, folder] = uigetfile(defaultFileName, 'Select Image');
if baseFileName == 0
	% User clicked the Cancel button.
	return;
end
filename = fullfile(folder, baseFileName);
handles.filename = filename;
guidata(hObject,handles)
% hObject    handle to target_button (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

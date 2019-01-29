function []=sticking()

screen=get(0,'screensize');
screen=screen(3:4);
p=1;
handle.figure=figure(...
    'Name', 'Sticking Coefficients',...
    'NumberTitle', 'off',...
    'color',[.94,.94,.94],...
    'position',[0*screen(1),0.02*screen(2),screen(1),0.9*screen(2)]);
%Axes
handle.axes=axes(...
    'units','normalized',...
    'position',[0.41,0.14,0.38,0.8]);


%Table
columnname={'K'};
columnformat={'numeric'};
columneditable= [true];
columnname2={'Coverage (ML)','S/So[K1]','S/So[K2]','S/So[K3]','S/So[K4]','S/So[K5]','S/So[K6]','S/So[K7]','S/So[K8]','S/So[K9]','S/So[K10]','S/So[K11]','S/So[K12]',...
    'S/So[K13]','S/So[K14]','S/So[K15]','S/So[K16]','S/So[K17]','S/So[K18]','S/So[K19]','S/So[K20]'};
rowname={'K1','K2','K3','K4','K5','K6','K7','K8','K9','K10','K11','K12',...
    'K13','K14','K15','K16','K17','K18','K19','K20'};
dat={[];[];[];[];[];[];[];[];[];[];[];[];...
    [];[];[];[];[];[];[];[]};
handle.table2=uitable(...
    'units','normalized',...
    'position',[0.85, 0.37,0.11,0.475],...
    'ColumnFormat', columnformat,...
    'ColumnName', columnname,...
    'ColumnEditable', columneditable,...
    'Data',dat,...
    'RowName', rowname);

handle.table=uitable(...
    'units','normalized',...
    'position', [0.039 0.07 0.25 0.25],...
    'ColumnName', columnname2,...
    'columnwidth',{100},...
    'ColumnFormat', columnformat,...
    'RowName', []);
uicontrol(...
    'style', 'text',...
    'units','normalized',...
    'string','Choose up to 20 values of K to plot S/So[theta;K] simultaneously',...
    'position',[0.84,0.85,0.12,0.1],...
    'fontsize',11)
% handle.usertable=uitable(...
%     'units','normalized',...
%     'position', [

uicontrol(...
    'style', 'text',...
    'units', 'normalized',...
    'string', 'S/So',...
    'position', [0.12,0.32,0.1,0.025]);
%plotit button
handle.plotit=uicontrol(...
    'style','pushbutton',...
    'units','normalized',...
    'position',[.85 .25 .1 .08],...
    'string','Plot');
%create coverage checkbox panel


%Associate callbacks
set(handle.plotit,'callback',{@plotmyplot});

%Textbox function
textbox
    function []=textbox()
handle.newtextbox=axes(...
    'units','normalized',...
    'position',[0.0125,0.37,0.32,0.58],...
    'xtick',[], 'ytick', [],...
    'xcolor', 'w', 'ycolor','w');
str(1)={'=======Sticking Coefficients======='};
str(2)= {'The change in sticking coefficient, s, with'};
str(3)={'coverage for precursor mediated adsorption'};
str(4)={'is characterized by the parameter K:'};
str(5)={''};
str(6)={'$$K = \frac{f^\prime_d}{f_a+f_d}$$'};
str(7)={''};
str(8)={'$$f^\prime_d$$ = extrinsic precursor desorption probability'};
str(9)={'$$f_a$$ =  intrinsic precursor adsorption probability'};
str(10)={'$$f_d$$ = intrinsic precursor desorption probability'};
str(11)={''};
str(12)={'Where the ratio of the sticking coefficient, s'};
str(13)={'to the initial sticking coefficnent, $$s_0$$ is'};
str(14)={'given by:'};
str(15)={''};
str(16)={'$$\frac{s(\theta)}{s_0}=[1+K(\frac{1}{\theta_{req}}-1)]^{-1}$$'};
str(17)={''};
str(18)={'where $$\theta_{req}$$ is set to $$\theta_{req}=(1-\theta)$$'}; 
str(19)={'(models nondissociative adsorption)'};

set(handle.figure,'currentaxes',handle.newtextbox);
ltxstr=text('interpreter','latex','string',str, 'units','normalized','position',[.05 .5],'fontsize',16);
    end


%Make plot
function plotmyplot(varargin)
    clear
    cla
    clc
    dat={[];[];[];[];[];[];[];[];[];[];[];[];...
    [];[];[];[];[];[];[];[]};
dat=get(handle.table2,'data');
K=cell2mat(get(handle.table2,'data'));

for i=1:length(dat)
    aa(i)=isempty(dat{i});
end
j=1;
for i=1:length(dat)
    if aa(i)==1
        dat{i}=[NaN];
    end

end
p=1;
for i=1:length(dat)
    aaa(i)=isnan(dat{i});
end

for i=1:length(dat)
    if aaa(i)==1
        dat{i}=[];
    end

end
for i=1:length(dat)
    aaaaa(i)=isempty(dat{i});
end

for i=1:length(aaaaa)
    
        if aaaaa(i)~=1
        lmnop(1,j)=i;
        j=j+1;
        end
end

K=cell2mat(dat);
p=1;

    for i=1:length(K)
        x=num2str(K(i,1));
        KK(i,1:length(x))=x;
    end


    set(handle.table2,'data',dat)

set(handle.figure,'currentaxes',handle.axes);
[sso,x]=sticky(K);
dat2=vertcat(x,sso);
dat3=dat2';
[r,c]=size(dat3);
p=1;
data4=cell(r,20);

lmnopp=lmnop+1;
p=1;
lmnopp=horzcat(1,lmnopp);
for i=1:length(lmnopp)
    for j=1:r
        data4{j,lmnopp(i)}=dat3(j,i);
    end
end
p=1;
set(handle.table,'ColumnName',columnname2)
set(handle.table,'Data',data4)
p=1;
plot(x,sso);
xlabel('Coverage (ML)');
ylabel('S/So');
title('Sticking Coefficient')



legend(KK)

legend('location','best')


axis([ 0 1 0 1]);
textbox;
end

function [sso,x]=sticky(K)
x=linspace(0,1);
for i=1:length(K);
    for j=1:length(x);
        sso(i,j)=1./(1+K(i).*(1./(1-x(j))-1));
    end
end
end
end 


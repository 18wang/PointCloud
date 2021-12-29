using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using System.IO;
using Kitware.VTK;
using System.Diagnostics;

namespace WindowsFormsApplication1
{
    public partial class Form1 : Form
    {
        public Form1()
        {
            InitializeComponent();
        }

        private void button1_Click(object sender, EventArgs e)
        {
            readData("bunny.pcd");
        }
        public void readCloud(string filename)
        {
            FileInfo myFile = new FileInfo(filename);
            string name = myFile.Name;
            FileStream fs = null;
            StreamReader sr = null;
            double[] xyz = new double[3];

            char[] chDelimiter = new char[] { ' ', '\t', ';', ',' };
            int cnt = 0;
            string sLineBuffer;
            string[] sXYZ;
            fs = new FileStream(filename, FileMode.Open, FileAccess.Read, FileShare.ReadWrite);
            sr = new StreamReader(fs);
            while (!sr.EndOfStream)
            {
                sLineBuffer = sr.ReadLine();
                cnt++;
                sXYZ = sLineBuffer.Split(chDelimiter, StringSplitOptions.RemoveEmptyEntries);
                if (sXYZ == null)
                {
                    MessageBox.Show("数据出错");
                    return;
                }
                xyz[0] = Convert.ToDouble(sXYZ[0]);
                xyz[1] = Convert.ToDouble(sXYZ[1]);
                xyz[2] = Convert.ToDouble(sXYZ[2]);
               // m_CloudDic[name].Add(new SAPoint(xyz[0], xyz[1], xyz[2]));

                //points.InsertNextPoint(xyz[0], xyz[1], xyz[2]);
            }
        }
        vtkPoints points;
        public vtkPolyData polydata;
        public vtkPolyData input;
        public vtkVertexGlyphFilter glyphFilter;
        public vtkPolyDataMapper volmapper;
        public vtkActor actor;
        vtkRenderer ren1 = null;
        vtkRenderWindow renWin = null;
        vtkRenderWindowInteractor renderWindowInteractor = null;

        vtkAreaPicker areaPicker;
        vtkPolyData selected;
        public void readData(string fileName)
        {
            points = new vtkPoints();
            FileInfo myfile = new FileInfo(fileName);
            string namekey = myfile.Name;
            //points = vtkPoints.New();
            FileStream fs = null;
            StreamReader sr = null;
            double[] xyz = new double[3];

            char[] chDelimiter = new char[] { ' ', '\t', ';', ',' };
            int cnt = 0;
            string sLineBuffer;
            string[] sXYZ;
            try
            {


                fs = new FileStream(fileName, FileMode.Open, FileAccess.Read, FileShare.ReadWrite);
                sr = new StreamReader(fs);
                while (!sr.EndOfStream)
                {
                    sLineBuffer = sr.ReadLine();
                    cnt++;
                    sXYZ = sLineBuffer.Split(chDelimiter, StringSplitOptions.RemoveEmptyEntries);
                    if (sXYZ == null)
                    {
                        MessageBox.Show("数据出错");
                        return;
                    }
                    xyz[0] = Convert.ToDouble(sXYZ[0]);
                    xyz[1] = Convert.ToDouble(sXYZ[1]);
                    xyz[2] = Convert.ToDouble(sXYZ[2]);
                    points.InsertNextPoint(xyz[0], xyz[1], xyz[2]);

                    //if (cnt > 30)
                    //    break;
                }

            }
            catch (Exception ex)
            {
                MessageBox.Show(ex.ToString());
            }
          
            polydata = vtkPolyData.New();
            polydata.SetPoints(points);



            //vtkIdFilter 生成id
            vtkIdFilter idFilter = vtkIdFilter.New();
            idFilter.SetInputConnection(polydata.GetProducerPort());
            idFilter.PointIdsOn();
            idFilter.CellIdsOn();
            idFilter.FieldDataOn();
            idFilter.SetIdsArrayName("OriginalIds");
            idFilter.Update();

            vtkLabeledDataMapper ldm = vtkLabeledDataMapper.New();
            ldm.SetInputConnection(idFilter.GetOutputPort());
            ldm.SetLabelModeToLabelFieldData();

            vtkActor2D pointLabels = vtkActor2D.New();
            pointLabels.SetMapper(ldm);

            //vtkDataSetSurfaceFilter surfaceFilter = vtkDataSetSurfaceFilter.New();
            //surfaceFilter.SetInputConnection(idFilter.GetOutputPort());
            //surfaceFilter.Update();
            //vtkPolyData input = surfaceFilter.GetOutput();

           

            glyphFilter = vtkVertexGlyphFilter.New();
            //glyphFilter.SetInputConnection(polydata.GetProducerPort());
            glyphFilter.SetInputConnection(idFilter.GetOutputPort());

            ////vtkdatasets datafilter = vtkDataSet.New();
            ////datafilter. 
            input = glyphFilter.GetOutput();

            vtkPolyDataMapper mapper = vtkPolyDataMapper.New();
           // mapper.SetInput(input);
           // mapper.ScalarVisibilityOff();
            mapper.SetInput(input);

            
            ////mapper.SetInput(surfaceFilter.GetOutput());
            //// The actor links the data pipeline to the rendering subsystem
            actor = vtkActor.New();
            actor.SetMapper(mapper);
            actor.GetProperty().SetColor(1, 0, 0);

            // Create components of the rendering subsystem
            //

            // Add the actors to the renderer, set the window size
            //
            ren1 = renderWindowControl1.RenderWindow.GetRenderers().GetFirstRenderer();
            renWin = renderWindowControl1.RenderWindow;
            //ren1.AddViewProp(pointLabels);
            ren1.AddViewProp(actor);
            //renWin.SetSize(250, 250);
            renWin.Render();
        }
        Kitware.VTK.vtkRenderWindowInteractor Interactor = null;
        Kitware.VTK.vtkObject.vtkObjectEventHandler InteractorHandler = null;
        Kitware.VTK.vtkInteractorStyleUser UserStyle = null;
        Kitware.VTK.vtkObject.vtkObjectEventHandler UserHandler = null;
        //初始化区域拾取功能
        private void button2_Click(object sender, EventArgs e)
        {

            ////picker = new Kitware.VTK.vtkPropPicker();   
            areaPicker = new vtkAreaPicker();
            renderWindowInteractor.SetPicker(areaPicker);
            renderWindowInteractor.SetRenderWindow(renWin);
            areaPicker.EndPickEvt +=pickCallback;

            renderWindowInteractor.Initialize();
            renderWindowInteractor.Start();
            //this.Interactor = this.renderWindowControl1.RenderWindow.GetInteractor();
            //this.InteractorHandler = new Kitware.VTK.vtkObject.vtkObjectEventHandler(Interactor_AnyEventHandler);
            //this.Interactor.AnyEvt += this.InteractorHandler;             

        }
        private void pickCallback(Kitware.VTK.vtkObject sender, Kitware.VTK.vtkObjectEventArgs e)
        {

            // vtkAreaPicker areaPicker = static_cast<vtkAreaPicker*>(caller);
            vtkAreaPicker areaPicker = (vtkAreaPicker)e.Caller;
            vtkPlanes  frustum =
                ((vtkAreaPicker)areaPicker).GetFrustum();

            vtkExtractGeometry extractGeometry =vtkExtractGeometry.New();
            extractGeometry.SetImplicitFunction(frustum);
            extractGeometry.SetInput(input);
            extractGeometry.Update();



            vtkVertexGlyphFilter glyphFilter1 =vtkVertexGlyphFilter.New();
            glyphFilter1.SetInputConnection(extractGeometry.GetOutputPort());
            glyphFilter1.Update();
            

            selected = glyphFilter1.GetOutput();
            vtkIdTypeArray ids = (vtkIdTypeArray)(selected.GetPointData().GetArray("OriginalIds"));

            for (int i = 0; i < selected.GetNumberOfPoints(); i++)
            {
                //打印选中点的ID
                //this.textEvents.AppendText(i + "," + ids.GetValue(i) +"\t\n");
            }
                //vtkPointData aset = selected.GetPointData();
                //int mm = aset.GetNumberOfArrays();

                //vtkPolyDataMapper selectMapper = vtkPolyDataMapper.New();
                //selectMapper.SetInput(selected);
                //selectMapper.ScalarVisibilityOff();



                //Debug.WriteLine(input.GetPoints().GetNumberOfPoints());
                //vtkPolyDataMapper afterselectMapper = vtkPolyDataMapper.New();
                //afterselectMapper.SetInput(input);
                //afterselectMapper.ScalarVisibilityOff();



                //vtkActor afterselectPoints = vtkActor.New();
                //afterselectPoints.SetMapper(afterselectMapper);
                //afterselectPoints.GetProperty().SetColor(0.75, 0.75, 0.75);
                //ren1.AddActor(afterselectPoints);

                vtkPolyDataMapper selectMapper = vtkPolyDataMapper.New();
            selectMapper.SetInput(selected);
            selectMapper.ScalarVisibilityOff();



            vtkActor selectPoints = vtkActor.New();
            selectPoints.SetMapper(selectMapper);
            selectPoints.GetProperty().SetColor(0.75, 0.75, 0.75);
            ren1.AddActor(selectPoints);

            for (int i = 0; i < selected.GetNumberOfPoints(); i++)
            {
                double[] p = new double[3];
                p = selected.GetPoint(i);
                //打印每个点的三维坐标             
               // this.textEvents.AppendText(i +","+ p[0] + "," + p[1] + "," + p[2] +"\t\n");
            }
            
            //MessageBox.Show("选取的点数：" + selected.GetNumberOfPoints().ToString());
           // MessageBox.Show("选取的单元数：" + selected.GetNumberOfCells().ToString());
        }
        //该函数每次只能删除一个点，并且删除后新的点集重新分配ID号，所以不能用。
        //void RealDeletePoint(vtkPoints origin, int delPId)
        //{
        //   // Debug.WriteLine("删除前的点数:" + origin.GetNumberOfPoints());
        //    vtkPoints newPoints = vtkPoints.New();

        //    for (int i = 0; i < origin.GetNumberOfPoints(); i++)
        //    {
                               
        //        if (i != delPId)
        //        {
        //            double[] p = origin.GetPoint(i);
        //            newPoints.InsertNextPoint(p[0], p[1], p[2]);
        //        }
                
        //    }
        //   // Debug.WriteLine("删除后的点数:" + newPoints.GetNumberOfPoints());
        //    origin.ShallowCopy(newPoints);
        //}
        void RealDeletePoint(vtkPoints origin, vtkIdTypeArray delPIds, int n)
        {
            Debug.WriteLine("删除前的点数:" + origin.GetNumberOfPoints());
            vtkPoints newPoints = vtkPoints.New();
            int j = 0;
            for (int i = 0; i < origin.GetNumberOfPoints(); i++)
            {
                
                    if (i != delPIds.GetValue(j))
                    {
                        double[] p = origin.GetPoint(i);
                        newPoints.InsertNextPoint(p[0], p[1], p[2]);
                    }
                    else if(i == delPIds.GetValue(j))
                    {
                        j++;
                    }
                
            }
            Debug.WriteLine("删除后的点数:" + newPoints.GetNumberOfPoints());
            origin.ShallowCopy(newPoints);
        }
        void Interactor_AnyEventHandler(Kitware.VTK.vtkObject sender, Kitware.VTK.vtkObjectEventArgs e)
        {
            this.PrintEvent(sender, e);
        }
        void PrintEvent(Kitware.VTK.vtkObject sender, Kitware.VTK.vtkObjectEventArgs e)
        {
            //int[] pos = this.Interactor.GetEventPosition();
            //string keysym = this.Interactor.GetKeySym();
            //sbyte keycode = this.Interactor.GetKeyCode();

            //string line = String.Format("{0} ({1},{2}) ('{3}',{4}) {5} data='0x{6:x8}'{7}",
            //  Kitware.VTK.vtkCommand.GetStringFromEventId(e.EventId),
            //  pos[0], pos[1],
            //  keysym, keycode,
            //  e.Caller.GetClassName(), e.CallData.ToInt32(), System.Environment.NewLine);

            //System.Diagnostics.Debug.Write(line);
            //this.textEvents.AppendText(line);
           // this.textEvents.Text=e.Caller.GetClassName().ToString();
        }
        Point start, end;
        void Interactor_LeftButtonDownHandler(Kitware.VTK.vtkObject sender, Kitware.VTK.vtkObjectEventArgs e)
        {
            int[] pos = this.renderWindowInteractor.GetEventPosition();
            start.X = pos[0];
            start.Y = pos[1];
            this.textBox1.Text = start.X.ToString() + "," + start.Y.ToString();
        }
        void Interactor_LeftButtonUpHandler(Kitware.VTK.vtkObject sender, Kitware.VTK.vtkObjectEventArgs e)
        {
            int[] pos = this.renderWindowInteractor.GetEventPosition();
            end.X = pos[0];
            end.Y = pos[1];
            this.textBox2.Text = end.X.ToString() + "," + end.Y.ToString();
        }
        private void showPick(Kitware.VTK.vtkObject sender, Kitware.VTK.vtkObjectEventArgs e)
        {
            //MessageBox.Show(e.ToString());
        }

        private void button3_Click(object sender, EventArgs e)
        {
            int n =areaPicker.AreaPick(start.X, start.Y, end.X, end.Y, ren1);
            //areaPicker.get
            vtkDataSet data = areaPicker.GetDataSet();
            
            MessageBox.Show(data.GetNumberOfPoints().ToString());
        }

        private void button4_Click(object sender, EventArgs e)
        {
            vtkIdTypeArray ids = (vtkIdTypeArray)(selected.GetPointData().GetArray("OriginalIds"));

            //Debug.WriteLine(input.GetPoints().GetNumberOfPoints());
            //for (int i = 0; i < selected.GetNumberOfPoints(); i++)
            //{
            //    // this.textEvents.AppendText(i + "," + ids.GetValue(i) + "\t\n");
            //    RealDeletePoint(input.GetPoints(), ids.GetValue(i));
            //}
            //Debug.WriteLine(input.GetPoints().GetNumberOfPoints());

            RealDeletePoint(input.GetPoints(), ids, selected.GetNumberOfPoints());

            vtkPolyDataMapper afterselectMapper = vtkPolyDataMapper.New();
            afterselectMapper.SetInput(input);
            afterselectMapper.ScalarVisibilityOff();



            vtkActor afterselectPoints = vtkActor.New();
            afterselectPoints.SetMapper(afterselectMapper);
            afterselectPoints.GetProperty().SetColor(0.5, 0.5, 0.5);
            ren1.AddActor(afterselectPoints);
            renWin.Render();
            
        }

        private void Form1_Load(object sender, EventArgs e)
        {
            ren1 = renderWindowControl1.RenderWindow.GetRenderers().GetFirstRenderer();
            renWin = renderWindowControl1.RenderWindow;
            renderWindowInteractor = this.renderWindowControl1.RenderWindow.GetInteractor();

            vtkInteractorStyleRubberBandPick style =
             vtkInteractorStyleRubberBandPick.New();

            // For vtkInteractorStyleTrackballCamera - use 'p' to pick at the current
            // mouse position
            //vtkSmartPointer<vtkInteractorStyleTrackballCamera> style =
            //  vtkSmartPointer<vtkInteractorStyleTrackballCamera>::New(); 
            //like   paraview
            style.SetCurrentRenderer(ren1);
            renderWindowInteractor.SetInteractorStyle(style);
        }
    }
}

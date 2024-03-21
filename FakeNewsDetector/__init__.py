using System;
using System.Collections;
using System.Configuration;
using System.Data;
using System.Linq;
using System.Web;
using System.Web.Security;
using System.Web.UI;
using System.Web.UI.HtmlControls;
using System.Web.UI.WebControls;
using System.Web.UI.WebControls.WebParts;
using System.Xml.Linq;
using System.IO;
using System.Data.SqlClient;

public partial class AddPhotos : System.Web.UI.Page
{
    SqlConnection con = new SqlConnection(ConfigurationManager.ConnectionStrings["TravelCon"].ConnectionString);
    string season;
    int month;
    protected void Page_Load(object sender, EventArgs e)
    {
        TextBox6.Text = DateTime.Now.ToString();
        DateTime dt = DateTime.Now;
        month = dt.Month;
        if (month == 12 || month == 1 || month == 2)
        {
            season = "Summer";
        }
        else if(month == 3 || month == 4 || month == 5)
        {
            season = "Autumn";
        }
        else if (month == 6 || month == 7 || month == 8)
        {
            season = "Winter";
        }
        else if (month == 9 || month == 10 || month == 11)
        {
            season = "Spring";
        }
    }
    protected void Button1_Click(object sender, EventArgs e)
    {
        FileUpload1.SaveAs(Server.MapPath("~/images/community/")+FileUpload1.FileName);
        string filepath = Server.MapPath("~/images/community/")+FileUpload1.FileName;
        string fname = FileUpload1.FileName;

        FileStream fs = new FileStream(filepath,FileMode.Open,FileAccess.ReadWrite);
        byte[] buffer = new byte[fs.Length];
        fs.Read(buffer,0,(int)fs.Length);
        fs.Close();

        con.Open();
        SqlCommand cmd = new SqlCommand("insert into community values('" + TextBox1.Text + "','" + TextBox2.Text 
                         + "','" + fname + "',@Photo,'" + TextBox3.Text + "','" + TextBox4.Text + "','" + TextBox5.Text 
                         + "','" + TextBox6.Text + "','" + TextBox7.Text + "','" + TextBox8.Text + "','" + season + "')",con);
        cmd.Parameters.AddWithValue("@Photo", buffer);
        cmd.ExecuteNonQuery();
        con.Close();
        Response.Write("<script>alert('Community-Contributed Photos Added!')</script>");
    }
}

//AddTourPackage.aspx
using System;
using System.Collections;
using System.Configuration;
using System.Data;
using System.Linq;
using System.Web;
using System.Web.Security;
using System.Web.UI;
using System.Web.UI.HtmlControls;
using System.Web.UI.WebControls;
using System.Web.UI.WebControls.WebParts;
using System.Xml.Linq;
using System.Data.SqlClient;
using System.Collections.Generic;

public partial class AddTourPackage : System.Web.UI.Page
{
    SqlConnection con = new SqlConnection(ConfigurationManager.ConnectionStrings["TravelCon"].ConnectionString);
    string topics;
    protected void Page_Load(object sender, EventArgs e)
    {

    }
    protected void CustomValidator1_ServerValidate(object source, ServerValidateEventArgs args)
    {
        if (DropDownList1.Text == "Select City")
        {
            args.IsValid = false;
        }
        else
        {
            args.IsValid = true;
        }
    }
    
    protected void CustomValidator3_ServerValidate(object source, ServerValidateEventArgs args)
    {
        if (DropDownList3.Text == "Select Season")
        {
            args.IsValid = false;
        }
        else
        {
            args.IsValid = true;
        }
    }
    protected void Button1_Click(object sender, EventArgs e)
    {
        con.Open();
        SqlCommand cmd = new SqlCommand("insert into travelogues values('" + TextBox1.Text + "','" + DropDownList1.Text 
                         + "','" + topics + "','" + TextBox2.Text + "','" + TextBox3.Text + "','" + TextBox4.Text 
                         + "','" + TextBox5.Text + "','" + TextBox6.Text + "','" + TextBox7.Text + "','" + TextBox8.Text 
                         + "','" + TextBox9.Text + "','" + DropDownList3.Text + "','"+0+"')",con);
        cmd.ExecuteNonQuery();
        con.Close();
        Response.Write("<script>alert('Tour Package Added Successfully!')</script>");
    }
    protected void CheckBoxList1_SelectedIndexChanged(object sender, EventArgs e)
    {
        List<string> lst1 = new List<string>();
        for (int i = 0; i < CheckBoxList1.Items.Count; i++)
        {
            if (CheckBoxList1.Items[i].Selected == true)
            {
                string str = Convert.ToString(CheckBoxList1.Items[i]);
                lst1.Add(str);
            }
        }
        topics = string.Join(",", lst1.ToArray());        
    }
}
//UserInterest.aspx
using System;
using System.Collections;
using System.Configuration;
using System.Data;
using System.Linq;
using System.Web;
using System.Web.Security;
using System.Web.UI;
using System.Web.UI.HtmlControls;
using System.Web.UI.WebControls;
using System.Web.UI.WebControls.WebParts;
using System.Xml.Linq;
using System.Data.SqlClient;
using System.Collections.Generic;

public partial class UserInterest : System.Web.UI.Page
{
    SqlConnection con = new SqlConnection(ConfigurationManager.ConnectionStrings["TravelCon"].ConnectionString);
    protected void Page_Load(object sender, EventArgs e)
    {
        Label2.Text = Session["uname"].ToString();
    }    
    protected void ListBox1_SelectedIndexChanged(object sender, EventArgs e)
    {
        TextBox2.Text = ListBox1.SelectedItem.Text;
    }
    protected void ListBox2_SelectedIndexChanged(object sender, EventArgs e)
    {
        TextBox1.Text = ListBox2.SelectedItem.Text;
    }
   
    protected void ListBox4_SelectedIndexChanged(object sender, EventArgs e)
    {
        TextBox6.Text = ListBox4.SelectedItem.Text;
    }
    protected void Button1_Click(object sender, EventArgs e)
    {
        Panel7.Visible = true;
        Panel8.Visible = true;
        Panel9.Visible = true;
        BindData();
        BindUserData();
        Bindcommunity();
    }

    protected void CheckBoxList1_SelectedIndexChanged(object sender, EventArgs e)
    {
        List<string> lst1 = new List<string>();
        for (int i = 0; i < CheckBoxList1.Items.Count; i++)
        {
            if (CheckBoxList1.Items[i].Selected == true)
            {
                string str = Convert.ToString(CheckBoxList1.Items[i]);
                lst1.Add(str);
            }
        }
        TextBox4.Text = string.Join(",", lst1.ToArray());        
    }
    protected void BindData()
    {
        DataSet ds = new DataSet();
        DataTable FromTable = new DataTable();
        con.Open();
        string cmdstr = "Select * from travelogues where (Departure = '"+TextBox1.Text+"' AND City = '"+TextBox2.Text+"') AND (Cost <= '"+TextBox3.Text+"' AND Season = '"+TextBox6.Text+"') AND Topics LIKE '%"+TextBox4.Text+"%' order by rank DESC";
        SqlCommand cmd = new SqlCommand(cmdstr, con);
        SqlDataAdapter adp = new SqlDataAdapter(cmd);
        adp.Fill(ds);
        GridView1.DataSource = ds.Tables[0];
        GridView1.DataBind();
        con.Close();
    }

    protected void BindUserData()
    {
        DataSet ds = new DataSet();
        DataTable FromTable = new DataTable();
        con.Open();
        string cmdstr = "Select * from UserPackage where (Departure = '" + TextBox1.Text + "' AND Destination = '" + TextBox2.Text + "') AND (Cost <= '" + TextBox3.Text + "' AND Season = '" + TextBox6.Text + "') AND TopicalInterest LIKE '%" + TextBox4.Text + "%' order by rank DESC";
        SqlCommand cmd = new SqlCommand(cmdstr, con);
        SqlDataAdapter adp = new SqlDataAdapter(cmd);
        adp.Fill(ds);
        GridView2.DataSource = ds.Tables[0];
        GridView2.DataBind();
        con.Close();
    }
    protected void Bindcommunity()
    {
        DataSet ds = new DataSet();
        DataTable FromTable = new DataTable();
        con.Open();
        string cmdstr = "Select * from community where (Place = '" + TextBox2.Text + "' AND Season = '" + TextBox6.Text + "') OR Date LIKE '%" + TextBox5.Text + "%'";
        SqlCommand cmd = new SqlCommand(cmdstr, con);
        SqlDataAdapter adp = new SqlDataAdapter(cmd);
        adp.Fill(ds);
        DataList1.DataSource = ds.Tables[0];
        DataList1.DataBind();
        con.Close();
    }
    protected void GridView1_RowCommand(object sender, GridViewCommandEventArgs e)
    {
        if (e.CommandName == "Select")
        {
           
            int x = Convert.ToInt32(e.CommandArgument);
            GridViewRow row = GridView1.Rows[x];
            string from = row.Cells[0].Text;
            string to = row.Cells[1].Text;
            string topics = row.Cells[2].Text;
            string poi1 = row.Cells[3].Text;
            string poi2 = row.Cells[4].Text;
            string poi3 = row.Cells[5].Text;
            string poi4 = row.Cells[6].Text;
            string time = row.Cells[9].Text;
            string cost = row.Cells[10].Text;
            string season = row.Cells[11].Text; 
            con.Open();
            SqlCommand cmd = new SqlCommand("select rank from travelogues where (Departure = '"+from+"' AND City = '"+to+"') AND (Topics = '"+topics+"' AND Cost = '"+ cost +"') AND Season = '"+season+"'",con);
            int rnk = Convert.ToInt32(cmd.ExecuteScalar());
            rnk++;
            SqlCommand cmm = new SqlCommand("update travelogues set rank = '" + rnk + "' where (Departure = '" + from + "' AND City = '" + to + "') AND (Topics = '" + topics + "' AND Cost = '" + cost + "') AND Season = '" + season + "'", con);
            cmm.ExecuteNonQuery();
            con.Close();
            Response.Redirect("UserSelectedPackage.aspx?from=" + from + "&to=" + to + "&topics=" + topics + "&i1=" + poi1 + "&i2=" + poi2 + "&i3=" + poi3 + "&i4=" + poi4 + "&time=" + time + "&cost=" + cost + "&season=" + season);
        }
    }
    protected void GridView2_RowCommand(object sender, GridViewCommandEventArgs e)
    {
        if (e.CommandName == "Select")
        {
            int x = Convert.ToInt32(e.CommandArgument);
            GridViewRow row = GridView2.Rows[x];
            string uname = row.Cells[0].Text;
            string from = row.Cells[1].Text;
            string to = row.Cells[2].Text;
            string topics = row.Cells[3].Text;
            string poi1 = row.Cells[4].Text;
            string poi2 = row.Cells[5].Text;
            string poi3 = row.Cells[6].Text;
            string poi4 = row.Cells[7].Text;
            string time = row.Cells[9].Text;
            string cost = row.Cells[10].Text;
            string season = row.Cells[11].Text;

            con.Open();
            SqlCommand cmd = new SqlCommand("select rank from UserPackage where (Departure = '" + from + "' AND Destination = '" + to + "') AND (TopicalInterest = '" + topics + "' AND Cost = '" + cost + "') AND (Season = '" + season + "' AND Username = '"+uname+"')", con);
            int rnk = Convert.ToInt32(cmd.ExecuteScalar());
            rnk++;
            SqlCommand cmm = new SqlCommand("update UserPackage set rank = '" + rnk + "' where (Departure = '" + from + "' AND Destination = '" + to + "') AND (TopicalInterest = '" + topics + "' AND Cost = '" + cost + "') AND (Season = '" + season + "' AND Username = '" + uname + "')", con);
            cmm.ExecuteNonQuery();
            con.Close();

            Response.Redirect("UserSelectedPackage.aspx?from=" + from + "&to=" + to + "&topics=" + topics + "&i1=" + poi1 + "&i2=" + poi2 + "&i3=" + poi3 + "&i4=" + poi4 + "&time=" + time + "&cost=" + cost + "&season=" + season);
        }
    }
}
